import RPi.GPIO as GPIO
import requests
import datetime
import time
import json


GPIO.setwarnings(False)

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)

# 기상청 API가 3시간 간격으로 업데이트하기에 시간 범위 계산
def getLastBaseTime(calBase):
    t = calBase.hour
    if t < 2:
        calBase = calBase - datetime.timedelta(days=1)
        calBase = calBase.replace(hour=23)
    else:
        calBase = calBase.replace(hour=t - (t + 1) % 3)
    return calBase

# 기상청 API 호출 함수
def call_weather_api():
    calBase = datetime.datetime.now()
    calBase = getLastBaseTime(calBase)

    datetime00 = calBase.strftime("%Y%m%d") + calBase.strftime("%H") + '00'
    datetime01 = (calBase + datetime.timedelta(hours=1)).strftime("%Y%m%d") + (calBase + datetime.timedelta(hours=1)).strftime("%H") + '00'
    datetime02 = (calBase + datetime.timedelta(hours=2)).strftime("%Y%m%d") + (calBase + datetime.timedelta(hours=2)).strftime("%H") + '00'
    datetime03 = (calBase + datetime.timedelta(hours=3)).strftime("%Y%m%d") + (calBase + datetime.timedelta(hours=3)).strftime("%H") + '00'

    datePart0 = datetime00[:8]  # "YYYYMMDD"
    timePart0 = datetime00[8:]  # "HH00"
    datePart1 = datetime01[:8]  # "YYYYMMDD"
    timePart1 = datetime01[8:]  # "HH00"
    datePart2 = datetime02[:8]  # "YYYYMMDD"
    timePart2 = datetime02[8:]  # "HH00"
    datePart3 = datetime03[:8]  # "YYYYMMDD"
    timePart3 = datetime03[8:]  # "HH00"



    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'  # URL
    queryParams = {
        'serviceKey': 'pfwPJqSsq35REx9xZhUJmvGHVuFCPWyLXHFabpDm0vvuJWJOKBauTxCFCektk6tHTTEwHUnoGB/9gek1IyD9ww==',
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': datePart0,
        'base_time': timePart0,
        'nx': '62',
        'ny': '123'
    }

    response = requests.get(url, params=queryParams)

    if response.status_code == 200:
        data = response.json()
        items = data['response']['body']['items']['item']

        # JSON 파일에서 필요한 조건 설정 : 현재시간 +3시간까지 비올확률 30%이상
        filteredItems = [
            item for item in items
            if (
                (item['fcstDate'] == datePart0 and item['fcstTime'] == timePart0) or
                (item['fcstDate'] == datePart1 and item['fcstTime'] == timePart1) or
                (item['fcstDate'] == datePart2 and item['fcstTime'] == timePart2) or
                (item['fcstDate'] == datePart3 and item['fcstTime'] == timePart3)
            ) and item['category'] == 'POP' and float(item['fcstValue']) >= 30
        ]
        
        weather_info = "" #초기화
        #결과 형식
        for item in filteredItems:
            print(f"{item['fcstDate']} {item['fcstTime']} 강수확률: {item['fcstValue']}%")
            weather_info += f"{item['fcstDate']} {item['fcstTime']} 강수확률: {item['fcstValue']}%\n"   
            #결과 형식 반환
            return weather_info
    else:
        print(f"Request failed with status code {response.status_code}")


# 카톡 API 문자전송
def call_kakao_api():
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer " "jdFdNlFXjeRiZmDjBDtLNwJfqYr-uJyzE81RYitWCinJXgAAAYkKv4iO"
    }
    data = {
        "template_object": json.dumps({ #전송형태 json으로 해야 제대로 인식함.
            "object_type": "text",
            "text": weather_info,
            "link": {
                "web_url": "https://developers.kakao.com",
                "mobile_web_url": "https://developers.kakao.com"
            },
            "button_title": "바로 확인"
        })
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    print(response.json())


# 초음파 거리 측정 함수
def measure_distance():
    print("def dis start")

    try:
        while True:
            GPIO.output(TRIG,True)
            time.sleep(0.00001)        # 10uS의 펄스 발생을 위한 딜레이
            GPIO.output(TRIG, False)
            while GPIO.input(ECHO)==0:
                start = time.time()     # Echo핀 상승 시간값 저장
            while GPIO.input(ECHO)==1:
                stop = time.time()      # Echo핀 하강 시간값 저장
            check_time = stop - start
            distance = check_time * 34300 / 2
            print("Distance : %.1f cm" % distance)
            time.sleep(0.4)
            
            # 거리 값을 반환
            return distance
            
    except KeyboardInterrupt:
        print("거리 측정 완료 ")
        GPIO.cleanup()
        
    


try:
    while True:
        # 거리 값을 측정
        distance = measure_distance()

        # 거리 값에 따라 동작을 수행
        if distance < 10:  # 일정 거리보다 가까워지면 동작 수행
            # 기상청 API 호출
            weather_info = call_weather_api()   
            #weather_info은 call_weather_api()의 return 값으로 변수 명은 달려져도 무방함. 단 아래에서 쓰고자하는 변수명과 동일해야됨.
            
            # 카카오 API 호출
            response = call_kakao_api()
            

    

except KeyboardInterrupt:
    # 프로그램 종료 시 GPIO 리소스 해제
    GPIO.cleanup()

