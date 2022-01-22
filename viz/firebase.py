import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
#Load dữ liệu học phần
data = pd.read_csv('CourseListdata.csv')
# data[['id', 'Mã học phần']]

#Load dữ liệu mở rộng
dataex = pd.read_csv('CourseListdataextend.csv')
# dataex[['id','Học phần điều kiện']]

# join 2 bảng dữ liệu
course=data.merge(dataex, on="id")
# Ghi du lieu
print(course)
df = pd.DataFrame(course)
df.to_csv('Course.csv')
# Up data to firebase
cred = credentials.Certificate('siscourse-firebase-adminsdk-rghqn-2861cb8a24.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection('Image')
# # Import data
# df = pd.read_csv('Course.csv')
# tmp = df.to_dict(orient='records')
# list(map(lambda x: doc_ref.add(x), tmp))
# Export Data
docs = doc_ref.stream()
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')