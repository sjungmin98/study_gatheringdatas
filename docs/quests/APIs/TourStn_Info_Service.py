import requests

url = 'http://apis.data.go.kr/1360000/TourStnInfoService1/getTourStnVilageFcst1'

# https://apis.data.go.kr/1360000/TourStnInfoService1/getTourStnVilageFcst1?
# serviceKey=oF8cvDrrW27C3TgVpKW9ax9JcOFDDBL%2BwlraX%2BGs9W5qYdA5jb0UnPfKCqV7BtR%2F1lHnKsfXRYlB7JZLJumIeA%3D%3D
# &pageNo=1
# &numOfRows=10
# &dataType=json
# &CURRENT_DATE=2019122010
# &HOUR=24
# &COURSE_ID=1

params = {'serviceKey' : 'oF8cvDrrW27C3TgVpKW9ax9JcOFDDBL+wlraX+Gs9W5qYdA5jb0UnPfKCqV7BtR/1lHnKsfXRYlB7JZLJumIeA=='
          ,'pageNo' : 1
          ,'numOfRows' : 10
          ,'dataType' : 'json'
          ,'CURRENT_DATE' : '2019122010'
          ,'HOUR' : '24'
          ,'COURSE_ID' : '1'}

# response = requests.get(url)
response = requests.get(url, params=params)

import json
contents = json.loads(response.content)

pass
#mongodb 저장
from pymongo import MongoClient
# mongodb에 접속 -> 자원에 대한 class
mongoClient = MongoClient("mongodb://localhost:27017")
# database 연결
database = mongoClient["data_go_kr"]
# collection 작업

collection = database['TourStn_Info_Service']
# insert 작업 진행
try:
    items = contents['response']['body']['items']['item']
    result = collection.insert_many(items)
except KeyError as e:
    print(contents)
pass