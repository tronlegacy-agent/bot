import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.document("人選之人─造浪者/19yDZvnES6sZoG923TE9")
doc = doc_ref.get()
result = doc.to_dict()
print(result["birth"])
#print("教師姓名："+result.get("name"))
#print("教師郵件：" + result["mail"])
