import requests

from bs4 import BeautifulSoup

url = "https://www1.pu.edu.tw/~tcyang/course.html"

Data = requests.get(url)
Data.encoding = "utf-8"
#print(Data.text)

sp = BeautifulSoup(Data.text, "html.parser")

result=sp.select(".team-box")
# print(result)
for x in result:
	print(x.find("h4").text)
	print(x.find("a").get("href"))
	print("https://www1.pu.edu.tw/~tcyang/"+ x.find("img").get("src"))
	print()

# print(result)
# info = ""

# for item in result:

# 	info += item.text + "\n\n"

# print(info)
# for x in result:
# 	print(x.text)
# 	print(x.get("href"))
# 	print()