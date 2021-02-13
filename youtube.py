# -*- coding: utf-8 -*- 
##API를 이용하여 유튜브 사이트 정보 크롤링

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from oauth2client.client import flow_from_clientsecrets
from ast import literal_eval
import time
from datetime import timedelta
import datetime
import os
import sys
import httplib2

print('---------------------시작---------------------')
CLIENT_SECRETS_FILE = "client_secrets.json" #사용자 인증정보를 설정
#사용자 인증정보를 가져오지 못할 때, 오류 메시지 출력
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
DEVELOPER_KEY = "AIzaSyByCLXH_dy05rnp2QTeVjb-i_sRW5tMXLw"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"

#사용자 인증 메시지 관련 코드
flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()



if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)


#build()함수를 이용하여 크롤링객체를 생성
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY,http=credentials.authorize(httplib2.Http()))

#########반복문 넣어서 ID값을 여러개 불러와야 함###############
### 사실상 아래 코드는 주석처리 해놓으면 될 것 같아.
## 유튜브 사용자 이름으로부터 ID값 얻어오기
#forUsername='채널 사용자 이름'
'''
id =youtube.channels().list(part="id", forUsername="AngrySmiile").execute()
real_id =[] # id값은 리스트로 보관
for id_result in id.get("items",[]): #get()함수를 통해 items 내 요소들을 리스트로써 불러온다.
    if id_result["kind"]=="youtube#channel":
        real_id.append("%s"%id_result['id'])
print(real_id)        
'''

##시간 설정 및 테스트
print('--------------------시간 설정 테스트 시작 ---------------------')
today = datetime.datetime.today()
set_time =str(today - timedelta(days=7))
set_time_again =set_time[:10]+'T'+set_time[11:19]+'Z' #RFC 3339 형식으로 시간 설정
print(set_time_again)
print(set_time)
print(today)
print(str(today-timedelta(days=20)))

#0~6 인덱스까지 총 7개 존재
print('--------------------ID 값 리스트에 정렬하기 테스트 시작---------------------')
ids=[]
ids.append('UCBkyj16n2snkRg1BAzpovXQ')#우왁굳
ids.append('UC-Zedn7a_RJyb5hUQ-aGZog')#머독인가
ids.append('UCb-y7YXK75lcU76lyFwBDgQ')#상윤쓰
ids.append('UCzRUMnhvhTg23u1QjQEJn5g')#이토끼
ids.append('UCQNE2JmbasNYbjGAcuBiRRg')#조코딩
ids.append('UCQ2O-iftmnlfrBuNsUUTofQ')#십오야
ids.append('UCvdvPu_7TTcrZz1nGh98Sqg')#오마르의삶
print(ids)


###################반복문을 통해서 채널마다 가져옴#######################
#채널 ID를 통해 해당 채널의 동영상들을 가져온다.
#order = 'date'를 통해 일자가 최신것을 먼저 가져온다
#maxResults = 정수 를 통해 최대 검색 갯수를 설정한다.
#publishedAfter ="시간대" 를 통해 언제 날짜것부터 가져올지를 정한다.
#channelId = 'channelid'를 통해 영상을 가져올 채널을 설정한다.

##############아래의 코드에서 비디오 ID는 제외하고 비디오 url을 넣어주면 될 것 같아.
##비디오 url = https://www.youtube.com/watch?v=비디오id 로 구성되네

##사실 아래 코드에서 결과적으로 얻고자 하는건 title, videoId 해서 2개 정도...
print('--------------------채널ID로 영상정보, title이름, video ID 찾기 테스트 시작 ---------------------')
videos = []
vidoeIds = []
search_response=[]
#channelId = ids[i]를 입력하자
for i in range(len(ids)):
    search_response.append(youtube.search().list(
            order = "date",
            part = "snippet",
            maxResults = 1 ,#최대 검색 갯수,
            publishedAfter = set_time_again, #지정된 시간 이후에 만든 리소스만 가져옴. 값은 RFC 3339 형식이 지정된 날짜-시간 값(1970-01-01T00:00:00Z)입니다.
            channelId = str(ids[i]) # 리스트에 저장된 id값을 하나씩 불러온다.
        
        ).execute())
    for search_result in search_response[i].get("items", []):
        if search_result["id"]["kind"] =="youtube#video":
            videos.append("%s(https://www.youtube.com/watch?v=%s)" %(search_result["snippet"]["title"], #videos 리스트에는 title과 videoId를 저장
                                    search_result["id"]["videoId"]))
            vidoeIds.append(search_result["id"]["videoId"])
print('비디오의 이름과 url만 제출합니다.\n'+str(videos))
print('비디오의 고유번호들 : '+str(vidoeIds))






###################위의 과정들이 해결될때 까지 잠시 봉인

##플레이리스트 생성은 1번만 하면 되는 거고
##플레이리스트에 동영상 넣기는 for문 돌려서 videoId받아와서 넣어야지 ~
'''
#플레이리스트 생성 
print('--------------------재생목록 생성하기 테스트 시작 ---------------------')
playlists_insert_response = youtube.playlists().insert(
  part="snippet,status",
  body=dict(
    snippet=dict(
      title=set_time[:19], # 플레이리스트 이름 지정
      description="A private playlist created with the YouTube API v3" # 내용
    ),
    status=dict(
      privacyStatus="private"
    )
  )
).execute()
#플레이리스트 ID 출력
print ("New playlist id: %s" % playlists_insert_response["id"])



#유튜브의 재생목록에 리소스(동영상) 추가
print('--------------------재생목록에 리소스 추가 테스트 시작---------------------')
playlistitems_list_request = []
for i in range(len(ids)):
    playlistitems_list_request.append(youtube.playlistItems().insert(
        part="snippet",
            body={
                    'snippet': {
                    'playlistId': str(playlists_insert_response["id"]),#해당 플레이리스트의 ID 
                    'resourceId': {
                            'kind': 'youtube#video', #추가할 리소스의 종류
                            'videoId':str(vidoeIds[i]) #추가할 리소스의 ID
                        }
                    #'position': 0
                    }
            }).execute())
'''



print('---------------------종료---------------------')
"""
ids=[]
ids.append('UCBkyj16n2snkRg1BAzpovXQ')
유튜버 동영상 목록
우왁굳 채널 ID = UCBkyj16n2snkRg1BAzpovXQ
머독 채널 ID =
안될과학 채널 ID = UCMc4EmuDxnHPc6pgGW-QWvQ
상윤쓰 채널 ID = UCb-y7YXK75lcU76lyFwBDgQ
동빈나 채널 ID = UChflhu32f5EUHlY7_SetNWw
십오야 채널 ID = UCQ2O-iftmnlfrBuNsUUTofQ
왼손코딩 채널 ID = UC0h8NzL2vllvp3PjdoYSK4g
조코딩 채널 ID = UCQNE2JmbasNYbjGAcuBiRRg
이토끼 채널 ID = UCzRUMnhvhTg23u1QjQEJn5g
오마르의 삶 채널 ID = UCvdvPu_7TTcrZz1nGh98Sqg
https://www.youtube.com/user/woowakgood/videos
https://www.youtube.com/user/AngrySmiile/videos
https://www.youtube.com/user/AngrySmiile/videos
https://www.youtube.com/c/tvNDENT/videos
https://www.youtube.com/channel/UC7qNMLmQ-qKEFvzHhzUFswg/videos
https://www.youtube.com/user/dlgksquf159/videos
https://www.youtube.com/c/%EC%97%B0%EB%91%90%EB%B6%80%ED%95%98%EC%9D%B4%EB%9D%BC%EC%9D%B4%ED%8A%B8/videos
"""


