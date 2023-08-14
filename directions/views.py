from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests  # requests 라이브러리를 이용하여 API 호출
from datetime import datetime
import copy
from .models import SubwayStationtime  # 실제로 사용 중인 SubwayStationtime 모델을 임포트해야 합니다.
import sys

class DirectionsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # 기존의 Normal과 Express 딕셔너리 코드를 이곳에 작성
        Normal = {
            "3호선": ["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"],
            "4호선": ["진접","오남","별내별가람","당고개","상계","노원", "창동","쌍문","수유","미아","미아사거리","길음","성신여대입구","한성대입구","혜화","동대문","동대문역사문화공원","충무로","명동","회현","서울역","숙대입구","삼각지","신용산","이촌","동작","총신대입구","사당","남테령","선바위","경마공원","대공원","과천","정부과천청사","인덕원","평촌","범계","금정","산본","수리산","대야미","반월","상록수","한대앞","고잔","초지","안산","신길온천","정왕","오이도"],
            "7호선": ["장암","도봉산","수락산","마들","노원","중계","하계","공릉","태릉입구","먹골","중화","상봉","면목","사가정","용마산","중곡","군자","어린이대공원","건대입구","뚝섬유원지","청담","강남구청","학동","논현","반포","고속터미널","내방","총신대입구","남성","숭실대입구","상도","장승배기","신대방삼거리","보라매","신풍","대림","남구로","가산디지털단지","철산","광명사거리","천왕","온수","까치울","부천종합운동장","춘의","신중동","부천시청","상동","삼산체육관","굴포천","부평구청","산곡","석남"],
            "8호선": ["암사","천호","강동구청","몽촌토성","잠실","석촌","송파","가락시장","문정","장지","복정","남위례","산성","남한산성입구","단대오거리","신흥","수진","모란"],
            "9호선": ["개화","김포공항","공항시장","신방화","마곡나루","양천향교","가양","증미","등촌","염창","신목동","선유도","당산","국회의사당","여의도","샛강","노량진","노들","흑석","동작","구반포","신반포","고속터미널","사평","신논현","언주","선정릉","삼성중앙","봉은사","종합운동장","삼전","석촌고분","석촌","송파나루","한성백제","올림픽공원","둔촌오륜","중앙보훈병원"],
        }

        Express = {
            "4호선" : ["당고개","사당","금정","산본","상록수","중앙","초지","안산","정왕","오이도"],
            "9호선" : ["김포공항","마곡나루","가양","염창","당산","여의도","노량진","동작","고속터미널","신논현","선정릉","봉은사","종합운동장","석촌","올림픽공원","중앙보훈병원"]
        }

        # Subway API를 호출하고 데이터를 받아오는 함수
        def call_subway_api():
            url = "http://127.0.0.1:8000/subways/"  # 실제 API 엔드포인트 URL로 대체해야 합니다.
    
            try:
                response = requests.get(url)
                response.raise_for_status()  # HTTP 요청이 성공적이지 않을 경우 예외를 발생시킵니다.
                data = response.json()       # JSON 응답 데이터를 파싱하여 딕셔너리로 변환합니다.
        
            # 데이터를 가공 또는 활용하는 로직을 추가하세요
            # data를 이용한 작업을 진행하세요
        
                return data  # 원하는 데이터를 반환합니다.
            except requests.exceptions.RequestException as e:
                print("API 요청 중 오류 발생:", e)
                return None

        # 모델에서 운행 시간을 가져오는 함수
        def get_operation_time_by_station_and_line(station_name, line_number):
            try:
                subway_data = SubwayStationtime.objects.get(station_name=station_name, line_number=line_number)
                operation_time = subway_data.operation_time
                return operation_time
            except SubwayStationtime.DoesNotExist:
                return None

        # Subway API를 호출하여 데이터 가져오기
        subway_data = call_subway_api()

        if subway_data is not None:
            if subway_data["express"] == 0:
                line_num_value = subway_data["line_num"]
                subway_line = Normal.get(line_num_value, [])
            else:
                line_num_value = subway_data["line_num"]
                subway_line = Express.get(line_num_value, [])

            base_sub_list = copy.deepcopy(subway_line)
            if subway_data["direction"] == 0:
                base_sub_list.reverse()

            target_element = subway_data["cur_station"]
            index_of_target = base_sub_list.index(target_element)

            if index_of_target >= 2:
                if subway_data["arrival_message"] == 0 or subway_data["arrival_message"] == 3:
                    index_of_target -= 1
                    base_sub_list = base_sub_list[index_of_target:]
                else:
                    base_sub_list = base_sub_list[index_of_target:]
            else:
                print("Error")
                sys.exit(1)

            subwithtime = [[x, -1, -1, -1] for x in base_sub_list]
            time_str = subway_data["msg_time"]
            datetime_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            hour = datetime_obj.hour
            minute = datetime_obj.minute
            second = datetime_obj.second
            time_list = [hour, minute, second]

            if subway_data["express"] == 0:
                if subway_data["arrival_message"] != 0:
                    for i in range(1, 5):
                        term_time = get_operation_time_by_station_and_line(base_sub_list[i], subway_data["line_num"])
                        if term_time is not None: #역간시간정보 있으면
                            mins,secs = map(int, term_time.split(":"))
                            time_list[1] += mins
                            time_list[2] += secs
                            time_list[2] += 25 #정차시간
                            if time_list[2] >= 120:
                                time_list[2] -= 120
                                time_list[1] += 2
                            elif time_list[2] >= 60:
                                time_list[2] -= 60
                                time_list[1] += 1
                            if time_list[1] >= 120:
                                time_list[0] += 2
                                time_list[1] -= 120
                            elif time_list[1] >= 60:
                                time_list[0] += 1
                                time_list[1] -= 60
                            if time_list[0] >= 24:
                                time_list[0] -= 24
                            subwithtime[i][1] = time_list[0]
                            subwithtime[i][2] = time_list[1]
                            subwithtime[i][3] = time_list[2]
                        else: #역간시간정보 없으면
                            pass
                elif subway_data["arrival_message"] == 0:
                    subwithtime[1][1] = time_list[0]
                    subwithtime[1][2] = time_list[1]
                    subwithtime[1][3] = time_list[2]
                    for i in range(2,5): # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
                        term_time = get_operation_time_by_station_and_line(base_sub_list[i], subway_data["line_num"])
                        if term_time is not None: #역간시간정보 있으면
                            mins,secs = map(int, term_time.split(":"))
                            time_list[1] += mins
                            time_list[2] += secs
                            time_list[2] += 25 #정차시간
                            if time_list[2] >= 120:
                                time_list[2] -= 120
                                time_list[1] += 2
                            elif time_list[2] >= 60:
                                time_list[2] -= 60
                                time_list[1] += 1
                            if time_list[1] >= 120:
                                time_list[0] += 2
                                time_list[1] -= 120
                            elif time_list[1] >= 60:
                                time_list[0] += 1
                                time_list[1] -= 60
                            if time_list[0] >= 24:
                                time_list[0] -= 24
                            subwithtime[i][1] = time_list[0]
                            subwithtime[i][2] = time_list[1]
                            subwithtime[i][3] = time_list[2]
                        else: #역간시간정보 없으면
                            pass
            else: #급행이면
                pass

            # 응답 데이터 구성
            return Response(subwithtime)

# class SubwayArrivalInfoView(APIView):
#     def get(self, request, format=None):
#         # Subways 앱의 API 엔드포인트에 요청을 보내서 실시간 데이터 가져오기
#         response = requests.get("URL_TO_SUBWAYS_APP_API")  # subways에서 정해준대로
#         realtime_data = response.json() if response.status_code == 200 else {}

#         # 여기서 필요한 정보를 추출하여 응답 데이터 구성
#         previous_station = "이전역"
#         next_station = realtime_data.get("next_station", "")
#         next_arrival = realtime_data.get("next_arrival", "10분 후")
#         next_next_arrival = realtime_data.get("next_next_arrival", "20분 후")
#         next_next_next_arrival = realtime_data.get("next_next_next_arrival", "30분 후")

#         response_data = {
#             "previous_station": previous_station,
#             "next_station": next_station,
#             "next_arrival": next_arrival,
#             "next_next_arrival": next_next_arrival,
#             "next_next_next_arrival": next_next_next_arrival,
#         }

#         return Response(response_data)
    
# from django.shortcuts import render
# from django.conf import settings
# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# TIME_KEY = settings.TIME_KEY 
# Create your views here.

# class SubwayAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         url = f"http://openapi.seoul.go.kr:8088/{TIME_KEY}/json/StationDstncReqreTimeHm/1/5/"
#         response = requests.get(url)
#         print(response.json())
#         return Response(response.json())

# subways 앱에서 정한 url에 따라 다름
# def get_subway_info():
#     url = "URL_TO_SUBWAYS_APP_API"  # subways 앱의 API 엔드포인트 URL
#     response = requests.get(url)
#     data = response.json()  # 응답 데이터를 JSON으로 파싱
#     return data
