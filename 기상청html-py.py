import requests
import datetime
import time

def getLastBaseTime(calBase):
    t = calBase.hour
    if t < 2:
        calBase = calBase - datetime.timedelta(days=1)
        calBase = calBase.replace(hour=23)
    else:
        calBase = calBase.replace(hour=t - (t + 1) % 3)
    return calBase

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

    filteredItems = [
        item for item in items
        if (
            (item['fcstDate'] == datePart0 and item['fcstTime'] == timePart0) or
            (item['fcstDate'] == datePart1 and item['fcstTime'] == timePart1) or
            (item['fcstDate'] == datePart2 and item['fcstTime'] == timePart2) or
            (item['fcstDate'] == datePart3 and item['fcstTime'] == timePart3)
        ) and item['category'] == 'POP' and float(item['fcstValue']) >= 30
    ]

    for item in filteredItems:
        print(f"{item['fcstDate']} {item['fcstTime']} 강수확률: {item['fcstValue']}%")
        
else:
    print(f"Request failed with status code {response.status_code}")
