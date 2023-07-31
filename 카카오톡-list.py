import requests
import json

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Bearer " "jdFdNlFXjeRiZmDjBDtLNwJfqYr-uJyzE81RYitWCinJXgAAAYkKv4iO"
}
data = {
    "template_object": json.dumps({
        "object_type": "list",
        "header_title": "비 예보",
        "header_link": {
            "web_url": "https://www.weather.go.kr/w/weather/forecast/short-term.do#dong/4113558000",
            "mobile_web_url": "https://www.weather.go.kr/w/weather/forecast/short-term.do#dong/4113558000",
            "android_execution_params": "main",
            "ios_execution_params": "main"
        },
        "contents": [
            {
                "title": "3시간 이내 강수 여부",
                "description": "rain3_ox",
                "image_url": "https://example.com/image1.jpg",
                "image_width": 640,
                "image_height": 640,
                "link": {
                    "web_url": "https://example.com/link1",
                    "mobile_web_url": "https://example.com/link1"
                }
            },
            {
                "title": "강수시간 및 강수확률",
                "description": "매거진",
                "image_url": "https://example.com/image2.jpg",
                "image_width": 640,
                "image_height": 640,
                "link": {
                    "web_url": "https://example.com/link2",
                    "mobile_web_url": "https://example.com/link2"
                }
            },
            {
                "title": "1일 이내 강수 여부",
                "description": "rain24_ox",
                "image_url": "https://example.com/image3.jpg",
                "image_width": 640,
                "image_height": 640,
                "link": {
                    "web_url": "https://example.com/link3",
                    "mobile_web_url": "https://example.com/link3"
                }
            }
        ],
        "buttons": [
            {
                "title": "웹으로 이동",
                "link": {
                    "web_url": "http://www.daum.net",
                    "mobile_web_url": "http://m.daum.net"
                }
            },
            {
                "title": "앱으로 이동",
                "link": {
                    "android_execution_params": "main",
                    "ios_execution_params": "main"
                }
            }
        ]
    })
}

response = requests.post(url, headers=headers, data=data)
print(response.status_code)
print(response.text)