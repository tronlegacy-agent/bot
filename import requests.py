import requests

url = "https://www1.pu.edu.tw/~tcyang/course.html"

Data = requests.get(url)

print(Data.text)
