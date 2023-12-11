import firebase_admin ,requests,make_response, jsonify

import requests
from bs4 import BeautifulSoup

from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from bs4 import BeautifulSoup

from flask import Flask, render_template,request

from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():

	homepage = "<h1>梅祐銘Python網頁<br>2023/11/30</h1>"

	homepage += "<a href=/mis>MIS</a><br>"

	homepage += "<a href=/today>顯示日期時間</a><br>"

	homepage += "<a href=/welcome?nick=tcyang>傳送使用者暱稱</a><br>"

	homepage += "<a href=/about>子青簡介網頁</a><br>"

	homepage +=  "<a href=/account>網頁表單</a>"

	homepage += "</br><a href=/wave>演員名單(年齡由小到大)</a>"

	homepage += "</br><a href=/spider>網路爬蟲</a>"
	
	homepage += "<br><a href=/movie>讀取開眼電影即將上映影片，寫入Firestore</a><br>"
     
	homepage += "<br><a href=/searchQ>即將上映電影查詢</a><br>"


	return homepage



@app.route("/mis")

def course():

	return "<h1>資訊管理導論</h1>"

@app.route("/today")

def today():

	now = datetime.now()

	return render_template("today.html", datetime = str(now))


@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")


@app.route("/welcome", methods=["GET", "POST"])
def welcome():

		user = request.values.get("nick")

		return render_template("welcome.html", name=user)

@app.route("/wave")
def read():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("人選之人─造浪者")    
    docs = collection_ref.order_by("birth", direction=firestore.Query.DESCENDING).get()    
    for doc in docs:         
        Result += "演員：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/spider")

def spider():
	info = ""
	url = "https://www1.pu.edu.tw/~tcyang/course.html"

	Data = requests.get(url)
	Data.encoding = "utf-8"
	#print(Data.text)

	sp = BeautifulSoup(Data.text, "html.parser")

	result=sp.select(".team-box")
	for x in result:
		info += "<a href="+x.find("a").get("href") +">" + x.find("h4").text + "</a><br>"
		info += x.find("p").text + "<br>"
		info += x.find("a").get("href") + "<br>"
		info += "<img src = https://www1.pu.edu.tw/~tcyang/" + x.find("img").get("src") + " width=200 height=auto ></img> + <br><br>"
	return info

@app.route("/movie")
def movie():
  url = "http://www.atmovies.com.tw/movie/next/"
  Data = requests.get(url)
  Data.encoding = "utf-8"
  sp = BeautifulSoup(Data.text, "html.parser")
  result=sp.select(".filmListAllX li")
  lastUpdate = sp.find("div", class_="smaller09").text[5:]

  for item in result:
    picture = item.find("img").get("src").replace(" ", "")
    title = item.find("div", class_="filmtitle").text
    movie_id = item.find("div", class_="filmtitle").find("a").get("href").replace("/", "").replace("movie", "")
    hyperlink = "http://www.atmovies.com.tw" + item.find("div", class_="filmtitle").find("a").get("href")
    show = item.find("div", class_="runtime").text.replace("上映日期：", "")
    show = show.replace("片長：", "")
    show = show.replace("分", "")
    showDate = show[0:10]
    showLength = show[13:]

    doc = {
        "title": title,
        "picture": picture,
        "hyperlink": hyperlink,
        "showDate": showDate,
        "showLength": showLength,
        "lastUpdate": lastUpdate
      }

    db = firestore.client()
    doc_ref = db.collection("電影").document(movie_id)
    doc_ref.set(doc)    
  return "近期上映電影已爬蟲及存檔完畢，網站最近更新日期為：" + lastUpdate

@app.route("/search")
def search():
    info = ""
    db = firestore.client()  
    docs = db.collection("電影").get() 
    for doc in docs:
        if "飛鴨" in doc.to_dict()["title"]:
            info += "片名：" + doc.to_dict()["title"] + "<br>" 
            info += "海報：" + doc.to_dict()["picture"] + "<br>"
            info += "影片介紹：" + doc.to_dict()["hyperlink"] + "<br>"
            info += "片長：" + doc.to_dict()["showLength"] + " 分鐘<br>" 
            info += "上映日期：" + doc.to_dict()["showDate"] + "<br><br>"           
    return info
@app.route("/searchQ", methods=["POST","GET"])
def searchQ():
    if request.method == "POST":
        MovieTitle = request.form["MovieTitle"]
        info = ""
        db = firestore.client()     
        collection_ref = db.collection("電影")
        docs = collection_ref.order_by("showDate").get()
        for doc in docs:
            if MovieTitle in doc.to_dict()["title"]: 
                info += "片名：" + doc.to_dict()["title"] + "<br>" 
                # info += "影片介紹：" + doc.to_dict()["hyperlink"] + "<br>"
				# info += "影片介紹：" + doc.to_dict()["hyperlink"]+"<a" + src=http://www.atmovies.com.tw/movie/fien22022452/ +"></a>" + "<br>"
                info += "影片介紹：" + "<a href='http://www.atmovies.com.tw/movie/fien22022452/'>" + doc.to_dict()["hyperlink"] + "</a>" + "<br>"

                info += "片長：" + doc.to_dict()["showLength"] + " 分鐘<br>" 
                info += "上映日期：" + doc.to_dict()["showDate"] + "<br><br>"          
        return info
    else:  
        return render_template("input.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    msg =  req.get("queryResult").get("queryText")
    info = "動作：" + action + "； 查詢內容：" + msg
    return make_response(jsonify({"fulfillmentText": info}))

@app.route("/movie_rate")
def movie_rate():
    url = "http://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".filmListAllX li")
    lastUpdate = sp.find(class_="smaller09").text[5:]

    for x in result:
        picture = x.find("img").get("src").replace(" ", "")
        title = x.find("img").get("alt")    
        movie_id = x.find("div", class_="filmtitle").find("a").get("href").replace("/", "").replace("movie", "")
        hyperlink = "http://www.atmovies.com.tw" + x.find("a").get("href")

        t = x.find(class_="runtime").text
        showDate = t[5:15]

        showLength = ""
        if "片長" in t:
            t1 = t.find("片長")
            t2 = t.find("分")
            showLength = t[t1+3:t2]

        r = x.find(class_="runtime").find("img")
        rate = ""
        if r != None:
            rr = r.get("src").replace("/images/cer_", "").replace(".gif", "")
            if rr == "G":
                rate = "普遍級"
            elif rr == "P":
                rate = "保護級"
            elif rr == "F2":
                rate = "輔12級"
            elif rr == "F5":
                rate = "輔15級"
            else:
                rate = "限制級"

        doc = {
            "title": title,
            "picture": picture,
            "hyperlink": hyperlink,
            "showDate": showDate,
            "showLength": showLength,
            "rate": rate,
            "lastUpdate": lastUpdate
        }

        db = firestore.client()
        doc_ref = db.collection("電影含分級").document(movie_id)
        doc_ref.set(doc)
    return "近期上映電影已爬蟲及存檔完畢，網站最近更新日期為：" + lastUpdate


		
if __name__ == "__main__":
	app.run()