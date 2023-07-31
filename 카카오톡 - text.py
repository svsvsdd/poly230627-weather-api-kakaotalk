import requests
import json

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Bearer " "jdFdNlFXjeRiZmDjBDtLNwJfqYr-uJyzE81RYitWCinJXgAAAYkKv4iO"
}
data = {
    "template_object": json.dumps({
        "object_type": "text",
        "text": "텍스트 영역입니다. 최대 200자 표시 가능합니다.",
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