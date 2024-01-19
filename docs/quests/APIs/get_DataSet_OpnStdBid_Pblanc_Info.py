import requests

url = 'http://apis.data.go.kr/1230000/PubDataOpnStdService/getDataSetOpnStdBidPblancInfo'

# https://apis.data.go.kr/1230000/PubDataOpnStdService/getDataSetOpnStdBidPblancInfo?
# serviceKey=oF8cvDrrW27C3TgVpKW9ax9JcOFDDBL%2BwlraX%2BGs9W5qYdA5jb0UnPfKCqV7BtR%2F1lHnKsfXRYlB7JZLJumIeA%3D%3D
# &pageNo=1
# &numOfRows=10
# &type=json
# &bidNtceBgnDt=201712010000
# &bidNtceEndDt=201712312359

params = {'serviceKey' : 'oF8cvDrrW27C3TgVpKW9ax9JcOFDDBL+wlraX+Gs9W5qYdA5jb0UnPfKCqV7BtR/1lHnKsfXRYlB7JZLJumIeA=='
          ,'pageNo' : 1
          ,'numOfRows' : 10
          ,'type' : 'json'
          ,'bidNtceBgnDt' : '201712010000'
          ,'bidNtceEndDt' : '201712312359'}

# response = requests.get(url)
response = requests.get(url, params=params)

import json
contents = json.loads(response.content)
print(response.content)
pass
#mongodb 저장
from pymongo import MongoClient
# mongodb에 접속 -> 자원에 대한 class
mongoClient = MongoClient("mongodb://localhost:27017")
# database 연결
database = mongoClient["data_go_kr"]
# collection 작업

collection = database['get_DataSet_OpnStdBid_Pblanc_Info']
# insert 작업 진행
result = collection.insert_many(contents['response']['body']['items'])
pass