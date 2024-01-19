# from : https://developers.naver.com/docs/serviceapi/search/news/news.md

import requests

# request API 요청
url = 'https://openapi.naver.com/v1/search/news'
params = {'query' : '인공지능'}
headers = {'X-Naver-Client-Id' : 'F4_GAlVWiHSQbxsW9zEv'
         , 'X-Naver-Client-Secret' : 'qovZIJ_Uwb'}

response = requests.get(url, params=params, headers=headers)

# response API 응답
response.content

# json을 변수로 변환
import json
contents = json.loads(response.content)

# MongoDB 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://localhost:27017")
database = mongoClient["search"]
collection1 = database['search_shop_info']
collection2 = database['search_shop_list']

# 'search_shop_info' collection에 데이터 삽입
info = {
    "lastBuildDate": contents['lastBuildDate'],
    "total": contents['total'],
    "start": contents['start'],
    "display": contents['display']
}
result_info = collection1.insert_one(info)

# 'search_shop_info'에서 생성된 _id 가져오기
inserted_info_id = result_info.inserted_id

# 'search_shop_list' collection에 데이터 삽입
for item in contents['items']:
    # type(contents['items'])
    # <class 'list'>
    item['relative_id'] = inserted_info_id  # relative_id로 'search_shop_info'의 _id 저장
    pass
    collection2.insert_one(item)