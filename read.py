# import firebase_admin
# from firebase_admin import credentials, firestore
# from google.cloud.firestore_v1.base_query import FieldFilter
 
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# collection_ref = db.collection("人選之人─造浪者")
# docs = collection_ref.where(filter=FieldFilter("birth","==",1966)).get()
#for doc in docs:
#    print("文件內容：{}".format(doc.to_dict()))

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

collection_ref = db.collection("人選之人─造浪者")
#docs = collection_ref.where(filter=FieldFilter("mail","==", "tcyang@pu.edu.tw")).get()
# docs = collection_ref.order_by("birth").limit(3).get()
docs = collection_ref.order_by("birth", direction=firestore.Query.DESCENDING).get()

for doc in docs:
    print("文件內容：{}".format(doc.to_dict()))
