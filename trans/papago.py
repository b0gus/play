import requests
 
# 네이버 파파고 api이용하기
url="https://openapi.naver.com/v1/papago/n2mt?source=en&target=ko&text="
 
text="Python is an easy to learn, powerful programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming. Python’s elegant syntax and dynamic typing, together with its interpreted nature, make it an ideal language for scripting and rapid application development in many areas on most platforms."
 
request_url = "https://openapi.naver.com/v1/papago/n2mt"
headers= {"X-Naver-Client-Id": "qCtqYG6hvJihYTqyxSJ0", "X-Naver-Client-Secret":"0bp5HS3MF5"}
params = {"source": "en", "target": "ko", "text": text}
response = requests.post(request_url, headers=headers, data=params)

result = response.json()["message"]["result"]["translatedText"]

print(result)
 