from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests  # requests 라이브러리를 이용하여 API 호출
from datetime import datetime
import copy
from .models import SubwayStation
import sys
from .serializers import DirectionsSerializer
import re
import os
import json
import pandas as pd

REALTIME_API_KEY = settings.REALTIME_API_KEY
# SUBWAYS_API_URL = "http://127.0.0.1:8000/api/subways"

def import_subway_data(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        data = pd.read_excel(excel_file, dtype={'operation_time': str})
        
        for _, row in data.iterrows():
            station = SubwayStation(
                line_number=row['line_number'],
                station_name=row['station_name'],
                eng_name=row['eng_name'],
                operation_time=row['operation_time'],
                exit=row['exit']
            )
            station.save()
        
        return render(request, 'directions/import_success.html')
    
    return render(request, 'directions/import_form.html')


class DirectionsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # 기존의 Normal과 Express 딕셔너리 코드를 이곳에 작성
        Normal = {
            "3호선": ["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"],
            "4호선": ["진접","오남","별내별가람","당고개","상계","노원","창동","쌍문","수유","미아","미아사거리","길음","성신여대입구","한성대입구","혜화","동대문","동대문역사문화공원","충무로","명동","회현","서울역","숙대입구","삼각지","신용산","이촌","동작","총신대입구","사당","남태령","선바위","경마공원","대공원","과천","정부과천청사","인덕원","평촌","범계","금정","산본","수리산","대야미","반월","상록수","한대앞","중앙","고잔","초지","안산","신길온천","정왕","오이도"],
            "7호선": ["장암","도봉산","수락산","마들","노원","중계","하계","공릉","태릉입구","먹골","중화","상봉","면목","사가정","용마산","중곡","군자","어린이대공원","건대입구","뚝섬유원지","청담","강남구청","학동","논현","반포","고속터미널","내방","총신대입구","남성","숭실대입구","상도","장승배기","신대방삼거리","보라매","신풍","대림","남구로","가산디지털단지","철산","광명사거리","천왕","온수","까치울","부천종합운동장","춘의","신중동","부천시청","상동","삼산체육관","굴포천","부평구청","산곡","석남"],
            "8호선": ["암사","천호","강동구청","몽촌토성","잠실","석촌","송파","가락시장","문정","장지","복정","남위례","산성","남한산성입구","단대오거리","신흥","수진","모란"],
            "9호선": ["개화","김포공항","공항시장","신방화","마곡나루","양천향교","가양","증미","등촌","염창","신목동","선유도","당산","국회의사당","여의도","샛강","노량진","노들","흑석","동작","구반포","신반포","고속터미널","사평","신논현","언주","선정릉","삼성중앙","봉은사","종합운동장","삼전","석촌고분","석촌","송파나루","한성백제","올림픽공원","둔촌오륜","중앙보훈병원"],
            "0호선": ["신사","논현","신논현","강남","양재","양재시민의숲","청계산입구","판교","정자","미금","동천","수지구청","성복","상현","광교중앙","광교"],
        }
        Express = {
            "4호선" : ["당고개","사당","금정","산본","상록수","중앙","초지","안산","정왕","오이도"],
            "9호선" : ["김포공항","마곡나루","가양","염창","당산","여의도","노량진","동작","고속터미널","신논현","선정릉","봉은사","종합운동장","석촌","올림픽공원","중앙보훈병원"],
        }

        # Subway API를 호출하고 데이터를 받아오는 함수
        # def call_subway_api():
        #     # directions 앱에서 받아온 Curlat와 Curlng 값
        #     Curlat = float(kwargs["Curlat"])
        #     Curlng = float(kwargs["Curlng"])

        #     # subways 앱의 API 엔드포인트 URL
        #     # subways_url = f"{SUBWAYS_API_URL}/Curlat={Curlat}&Curlng={Curlng}"
        #     subways_url = "http://127.0.0.1:8000/api/subways/37.49697/127.122720/"  # 실제 API 엔드포인트 URL로 대체해야 합니다.


        #     try:
        #         sbw_response = requests.get(subways_url)
        #         sbw_data = sbw_response.json()
        #         result_data = sbw_data["result_data"]
        #     except json.JSONDecodeError as e:
        #         result_data = []  # 빈 리스트로 초기화하여 에러 처리

        #     return Response({"result_data": result_data})
        #     # Curlat = float(kwargs["Curlat"])
        #     # Curlng = float(kwargs["Curlng"])

        #     # url = "http://127.0.0.1:8000/api/subways/{}/{}/".format(Curlat, Curlng)  # 실제 API 엔드포인트 URL로 대체해야 합니다.
    
        #     # try:
        #     #     response = requests.get(url)
        #     #     response.raise_for_status()  # HTTP 요청이 성공적이지 않을 경우 예외를 발생시킵니다.
        #     #     data = response.json()       # JSON 응답 데이터를 파싱하여 딕셔너리로 변환합니다.
        
        #     # 데이터를 가공 또는 활용하는 로직을 추가하세요
        #     # data를 이용한 작업을 진행하세요
        
        #     #     return data  # 원하는 데이터를 반환합니다.
        #     # except requests.exceptions.RequestException as e:
        #     #     print("API 요청 중 오류 발생:", e)
        #     #     return None

        # 모델에서 운행 시간을 가져오는 함수
        def get_operation_time_by_station_and_line(station_name, line_number):
            try:
                subway_data = SubwayStation.objects.get(station_name=station_name, line_number=line_number)
                operation_time = subway_data.operation_time
                return operation_time
            except SubwayStation.DoesNotExist:
                return None
        def get_eng_by_station_and_line(station_name, line_number):
            try:
                subway_data = SubwayStation.objects.get(station_name=station_name, line_number=line_number)
                eng_name = subway_data.eng_name
                return eng_name
            except SubwayStation.DoesNotExist:
                return None
        def get_exit_by_station_and_line(station_name, line_number):
            try:
                subway_data = SubwayStation.objects.get(station_name=station_name, line_number=line_number)
                exit = subway_data.exit
                return exit
            except SubwayStation.DoesNotExist:
                return None
            
        # 급행일시에는 중간에 있는 놈들을 불러모아야됨
        def get_stations_between(subway_line, start_station, end_station, direction):
            line_stations = Normal.get(subway_line, [])
            
            if start_station in line_stations and end_station in line_stations:
                start_index = line_stations.index(start_station)
                end_index = line_stations.index(end_station)
        
                if direction == 1: #하행이면 (순리)
                    stations_between = line_stations[start_index:end_index + 1]
                    return stations_between
                else: #상행이면 (역리)
                    stations_between = line_stations[end_index:start_index + 1]
                    return stations_between[::-1]  # Reverse the list
        
            else:
                return []

        current_dir = os.path.dirname(os.path.abspath(__file__))

        name2Id_path = os.path.join(current_dir, 'name2Id.json')

        with open(name2Id_path, 'r', encoding='utf-8') as json_file:
            name2Id = json.load(json_file)
        
        # # Subway API를 호출하여 데이터 가져오기
        # # toomuch_data = call_subway_api()
        # toomuch_data = {
        #     "result_data": [
        #         {
        #             "station_num": "3호선",
        #             "station_list": [
        #                 "수서",
        #                 "가락시장",
        #                 "경찰병원",
        #                 "오금"
        #             ],
        #             "trains": [
        #                 {
        #                     "line_num": "3호선",
        #                     "direction": "0",
        #                     "express": "0",
        #                     "arrival_message": "2",
        #                     "cur_station": "가락시장",
        #                     "endstation": "대치",
        #                     "msg_time": "2023-08-17 17:39:23",
        #                     "train_num": "3253"
        #                 }
        #             ]
        #         },
        #         {
        #             "station_num": "8호선",
        #             "station_list": [
        #                 "석촌",
        #                 "송파",
        #                 "가락시장",
        #                 "문정"
        #             ],
        #             "trains": [
        #                 {
        #                     "line_num": "8호선",
        #                     "direction": "0",
        #                     "express": "0",
        #                     "arrival_message": "1",
        #                     "cur_station": "잠실",
        #                     "endstation": "암사",
        #                     "msg_time": "2023-08-17 17:39:30",
        #                     "train_num": "8190"
        #                 },
        #                 {
        #                     "line_num": "신분당선",
        #                     "direction": "1",
        #                     "express": "0",
        #                     "arrival_message": "2",
        #                     "cur_station": "양재시민의숲",
        #                     "endstation": "정자",
        #                     "msg_time": "2023-08-17 17:39:34",
        #                     "train_num": "818"
        #                 }
        #             ]
        #         }
        #     ]
        # }
        # # 주어진 데이터에서 특정 train_num을 가진 딕셔너리 추출
        
        # # # target_train_num 
        # target_train_num = kwargs["train_num"] 
        # # print(target_train_num)
        # subway_data = None

        # for entry in toomuch_data["result_data"]:
        #     for train in entry["trains"]:
        #         if train["train_num"] == target_train_num:
        #             subway_data = train
        #             break

        # 대신 더미데이터
        # subway_data = {
        #     "line_num": "3호선", #(subwayNm)
        #     "direction": "0", #(updnLine) (0 : 상행/내선, 1 : 하행/외선)
        #     "express": "0", #(directAt) (1:급행, 0:아님)
        #     "arrival_message": "1", #(trainSttus) (0:진입 1:도착, 2:출발, 3:전역출발)
        #     "cur_station": "원당", #(statnNm)
        #     "endstation": "정발산", #(statnTnm)
        #     "msg_time": "2023-08-11 10:51:42" #(recptnDt),
        # }

        # 프로토타입
        # subway_data = {
        #     "line_num": request.data.get("line_num"),
        #     "direction": request.data.get("direction"),
        #     "express": request.data.get("express"),
        #     "arrival_message": request.data.get("arrival_message"),
        #     "cur_station": request.data.get("cur_station"),
        #     "endstation": request.data.get("endstation"),
        #     "msg_time": request.data.get("msg_time"),
        #     "train_num": request.data.get("train_num"),
        # }

        subway_nm = request.data.get("subway_nm")
        trainNo = request.data.get("trainNo")
        # subway_nm = "신분당선"
        # trainNo = "23"
        # {
        #     "arrival_message": "0",
        #     "cur_station": "양재시민의숲",
        #     "direction": "1",
        #     "endstation": "광교",
        #     "express": "0",
        #     "line_num": "신분당선",
        #     "msg_time": "2023-08-17 23:28:27",
        #     "train_num":"23"
        # }

        url = f"http://swopenAPI.seoul.go.kr/api/subway/{REALTIME_API_KEY}/json/realtimePosition/0/50/{subway_nm}"
        response = requests.get(url)
        data = response.json()
        
        if 'realtimePositionList' in data:
            realtime_position_list = data['realtimePositionList']

            for entry in realtime_position_list: # 호선 받은 실시간 지하철 위치정보중에 지하철 하나가 entry
                if trainNo==entry["trainNo"]: # 그 지하철의 ID가 내가 찾고 있는 ID 라면 (프론트에서 지정해준)
                    subway_data = {
                        "line_num": entry["subwayNm"],
                        "direction": entry["updnLine"],
                        "express": entry["directAt"],
                        "arrival_message": entry["trainSttus"],
                        "cur_station": entry["statnNm"],
                        "endstation": entry["statnTnm"],
                        "msg_time": entry["recptnDt"],
                        "train_num": entry["trainNo"]
                    }
        # 에상되는 문제점: subways의 views에서는 인접 4개의 역을 뒤져서 발견한 결관데 나는 그 지하철을 호선 전체에서 뒤져야되는데 10개만 뒤져서 확률상 발견될 수 있을까
        # 해결책: api 호출을 그 결과게시판인지 뭔지에 올려서 api 무한대로 만들고 0/100/ 그냥 찍어버린다

        # subway_data = {
        #     "arrival_message": "0",
        #     "cur_station": "양재시민의숲",
        #     "direction": "1",
        #     "endstation": "광교",
        #     "express": "0",
        #     "line_num": "신분당선",
        #     "msg_time": "2023-08-17 23:28:27",
        #     "train_num":"23",
        # }

        if subway_data["line_num"]=="신분당선":
            subway_data["line_num"] = "0호선"

        if subway_data is not None:
            if int(subway_data["express"]) == 0:
                line_num_value = subway_data["line_num"]
                subway_line = Normal.get(line_num_value, [])
            else:
                line_num_value = subway_data["line_num"]
                subway_line = Express.get(line_num_value, [])

            base_sub_list = copy.deepcopy(subway_line)
            if int(subway_data["direction"]) == 0:
                base_sub_list.reverse()

            # 0진입: cur==다음역 : list에서 cur station 이전역을 start로 짜되, msg time을 index1로 설정하고 그 뒤부터 time더해주기
            # 1도착: cur==현재역 : list에서 cur station 을 start로 짜되, index 1 = msg time + time 더해줘서 cur 뒤 4개 입력.
            # 2출발: cur==이전역 : list에서 cur station 을 start로 짜되, index 1 = msg time + time 더해줘서 cur 뒤 4개 입력.
            # 3전역 출발: cur==이전역 : list에서 cur station 이전역을 start로 짜되, index 1 = msg time + time 더해줘서 cur 뒤 4개 입력. 
            target_element = subway_data["cur_station"]
            index_of_target = base_sub_list.index(target_element)
            end_element = subway_data["endstation"]
            index_of_end = base_sub_list.index(end_element)

            if index_of_target >= 2:
                if int(subway_data["arrival_message"]) == 0 or int(subway_data["arrival_message"]) == 3: #진입이나 전역출발이라면
                    index_of_target -= 1
                    base_sub_list = base_sub_list[index_of_target:index_of_end+1]
                else:
                    base_sub_list = base_sub_list[index_of_target:index_of_end+1]
            else:
                #이전역이나 현재역이 첫역이라는 소리이기 때문에 에러 띄우고 종료
                print("Error")
                sys.exit(1)
            

            #msg_time 저장받아야됨 time_list에.
            #최종리스트가 subwithtime
            line_number_digits = re.findall(r'\d+', subway_data["line_num"])
            ln = int(line_number_digits[0])
            subwithtime = [[-1, x, "o", -1, -1, -1, -1, -1] for x in base_sub_list] #[0]은 호선, [1]은 역이름, [2]는 영어이름, [3]은 도착시 [4]는 도착분 [5]은 도착초, [6]은 출구, [7]은 환승노선
            for i in subwithtime:
                i[7] = sorted(name2Id[i[1]])
                i[0] = subway_data["line_num"]
                i[2] = get_eng_by_station_and_line(i[1],ln)
                i[6] = get_exit_by_station_and_line(i[1],ln)
        
            time_str = subway_data["msg_time"]
            datetime_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            hour = datetime_obj.hour
            minute = datetime_obj.minute
            second = datetime_obj.second
            time_list = [hour, minute, second]  # 시간, 분, 초를 리스트로 저장

            # return Response(subwithtime)
            

            # line_number_digits = re.findall(r'\d+', subway_data["line_num"])
            if line_number_digits: # 호선이 숫자라면
                # ln = int(line_number_digits[0]) # 호선 추출
                if int(subway_data["express"]) == 0:  # 완행이라면
                    if int(subway_data["direction"]) == 1: #하행 (순리대로) (자기까지 오는 시간이 자신의 termtime)
                        if int(subway_data["arrival_message"]) != 0:  # 진입이 아니라면
                            for i in range(1, len(subwithtime)):   # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
                                term_time = get_operation_time_by_station_and_line(base_sub_list[i], ln)
                                if term_time is not None: #역간시간정보 있으면
                                    mins,secs,trash = map(int, term_time.split(":"))
                                    time_list[1] += mins
                                    time_list[2] += secs
                                    time_list[2] += 30 #정차시간
                                    while(time_list[2]>=60):
                                        time_list[2] -= 60
                                        time_list[1] += 1
                                        if time_list[1]>=60:
                                            time_list[1] -= 60
                                            time_list[0] += 1
                                            if time_list[0]>=24:
                                                time_list[0] -=24
                                    while(time_list[1]>=60):
                                        time_list[1] -= 60
                                        time_list[0] += 1
                                        if time_list[0]>=24:
                                            time_list[0] -=24
                                    subwithtime[i][3] = time_list[0]
                                    subwithtime[i][4] = time_list[1]
                                    subwithtime[i][5] = time_list[2]
                                else: #역간시간정보 없으면
                                    pass
                        elif int(subway_data["arrival_message"]) == 0:  # 진입이라면
                            subwithtime[1][3] = time_list[0]
                            subwithtime[1][4] = time_list[1]
                            subwithtime[1][5] = time_list[2]
                            for i in range(2, len(subwithtime)): # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
                                term_time = get_operation_time_by_station_and_line(base_sub_list[i], ln)
                                if term_time is not None: #역간시간정보 있으면
                                    mins,secs,trash = map(int, term_time.split(":"))
                                    time_list[1] += mins
                                    time_list[2] += secs
                                    time_list[2] += 30 #정차시간
                                    while(time_list[2]>=60):
                                        time_list[2] -= 60
                                        time_list[1] += 1
                                        if time_list[1]>=60:
                                            time_list[1] -= 60
                                            time_list[0] += 1
                                            if time_list[0]>=24:
                                                time_list[0] -=24
                                    while(time_list[1]>=60):
                                        time_list[1] -= 60
                                        time_list[0] += 1
                                        if time_list[0]>=24:
                                            time_list[0] -=24
                                    subwithtime[i][3] = time_list[0]
                                    subwithtime[i][4] = time_list[1]
                                    subwithtime[i][5] = time_list[2]
                                else: #역간시간정보 없으면
                                    pass
                    else: # 상행이라면 (역리대로) (자기까지 오는 시간이 i-1의 termtime)
                        if int(subway_data["arrival_message"]) != 0:  # 진입이 아니라면
                            for i in range(1, len(subwithtime)):   # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
                                term_time = get_operation_time_by_station_and_line(base_sub_list[i-1], ln)
                                if term_time is not None: #역간시간정보 있으면
                                    mins,secs,trash = map(int, term_time.split(":"))
                                    time_list[1] += mins
                                    time_list[2] += secs
                                    time_list[2] += 30 #정차시간
                                    while(time_list[2]>=60):
                                        time_list[2] -= 60
                                        time_list[1] += 1
                                        if time_list[1]>=60:
                                            time_list[1] -= 60
                                            time_list[0] += 1
                                            if time_list[0]>=24:
                                                time_list[0] -=24
                                    while(time_list[1]>=60):
                                        time_list[1] -= 60
                                        time_list[0] += 1
                                        if time_list[0]>=24:
                                            time_list[0] -=24
                                    subwithtime[i][3] = time_list[0]
                                    subwithtime[i][4] = time_list[1]
                                    subwithtime[i][5] = time_list[2]
                                else: #역간시간정보 없으면
                                    pass
                        elif int(subway_data["arrival_message"]) == 0:  # 진입이라면
                            subwithtime[1][3] = time_list[0]
                            subwithtime[1][4] = time_list[1]
                            subwithtime[1][5] = time_list[2]
                            for i in range(2, len(subwithtime)): # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
                                term_time = get_operation_time_by_station_and_line(base_sub_list[i-1], ln)
                                if term_time is not None: #역간시간정보 있으면
                                    mins,secs,trash = map(int, term_time.split(":"))
                                    time_list[1] += mins
                                    time_list[2] += secs
                                    time_list[2] += 30 #정차시간
                                    while(time_list[2]>=60):
                                        time_list[2] -= 60
                                        time_list[1] += 1
                                        if time_list[1]>=60:
                                            time_list[1] -= 60
                                            time_list[0] += 1
                                            if time_list[0]>=24:
                                                time_list[0] -=24
                                    while(time_list[1]>=60):
                                        time_list[1] -= 60
                                        time_list[0] += 1
                                        if time_list[0]>=24:
                                            time_list[0] -=24
                                    subwithtime[i][3] = time_list[0]
                                    subwithtime[i][4] = time_list[1]
                                    subwithtime[i][5] = time_list[2]
                                else: #역간시간정보 없으면
                                    pass
                else: #급행이면
                    term_min = 0
                    term_sec = 0
                    if int(subway_data["direction"]) == 1: #하행 (순리대로) (자기까지 오는 시간이 자신의 termtime)
                        if int(subway_data["arrival_message"]) != 0:  # 진입이 아니라면
                            for i in range(1, len(subwithtime)):   # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
                                term_stations = get_stations_between(subway_data["line_num"], base_sub_list[i-1], base_sub_list[i], int(subway_data["direction"]))
                                for j in range(1, len(term_stations)):
                                    term_time = get_operation_time_by_station_and_line(term_stations[j], ln)
                                    if term_time is not None: #역간시간정보 있으면
                                        mins,secs,trash = map(int, term_time.split(":"))
                                        term_min += mins
                                        term_sec += secs
                                    else: #역간시간정보 없으면
                                        pass
                                time_list[1] += term_min
                                time_list[2] += term_sec
                                time_list[2] += 30 # 정차시간
                                while(time_list[2]>=60):
                                    time_list[2] -= 60
                                    time_list[1] += 1
                                    if time_list[1]>=60:
                                        time_list[1] -= 60
                                        time_list[0] += 1
                                        if time_list[0]>=24:
                                            time_list[0] -=24
                                while(time_list[1]>=60):
                                    time_list[1] -= 60
                                    time_list[0] += 1
                                    if time_list[0]>=24:
                                        time_list[0] -=24
                                subwithtime[i][3] = time_list[0]
                                subwithtime[i][4] = time_list[1]
                                subwithtime[i][5] = time_list[2]                        
                        elif int(subway_data["arrival_message"]) == 0:  # 진입이라면
                            subwithtime[1][3] = time_list[0]
                            subwithtime[1][4] = time_list[1]
                            subwithtime[1][5] = time_list[2]
                            for i in range(2,len(subwithtime)): # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
                                term_stations = get_stations_between(subway_data["line_num"], base_sub_list[i-1], base_sub_list[i], int(subway_data["direction"]))
                                for j in range(1, len(term_stations)):
                                    term_time = get_operation_time_by_station_and_line(term_stations[j], ln)
                                    if term_time is not None: #역간시간정보 있으면
                                        mins,secs,trash = map(int, term_time.split(":"))
                                        term_min += mins
                                        term_sec += secs
                                    else: #역간시간정보 없으면
                                        pass
                                time_list[1] += term_min
                                time_list[2] += term_sec
                                time_list[2] += 30 # 정차시간
                                while(time_list[2]>=60):
                                    time_list[2] -= 60
                                    time_list[1] += 1
                                    if time_list[1]>=60:
                                        time_list[1] -= 60
                                        time_list[0] += 1
                                        if time_list[0]>=24:
                                            time_list[0] -=24
                                while(time_list[1]>=60):
                                    time_list[1] -= 60
                                    time_list[0] += 1
                                    if time_list[0]>=24:
                                        time_list[0] -=24
                                subwithtime[i][3] = time_list[0]
                                subwithtime[i][4] = time_list[1]
                                subwithtime[i][5] = time_list[2]
                    else: # 상행이라면 (역리대로) (자기까지 오는 시간이 i-1의 termtime)
                        if int(subway_data["arrival_message"]) != 0:  # 진입이 아니라면
                            for i in range(1, len(subwithtime)):   # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
                                term_stations = get_stations_between(subway_data["line_num"], base_sub_list[i-1], base_sub_list[i], int(subway_data["direction"]))
                                for j in range(len(term_stations)-1):
                                    term_time = get_operation_time_by_station_and_line(term_stations[j], ln)
                                    if term_time is not None: #역간시간정보 있으면
                                        mins,secs,trash = map(int, term_time.split(":"))
                                        term_min += mins
                                        term_sec += secs
                                    else: #역간시간정보 없으면
                                        pass
                                time_list[1] += term_min
                                time_list[2] += term_sec
                                time_list[2] += 30 # 정차시간
                                while(time_list[2]>=60):
                                    time_list[2] -= 60
                                    time_list[1] += 1
                                    if time_list[1]>=60:
                                        time_list[1] -= 60
                                        time_list[0] += 1
                                        if time_list[0]>=24:
                                            time_list[0] -=24
                                while(time_list[1]>=60):
                                    time_list[1] -= 60
                                    time_list[0] += 1
                                    if time_list[0]>=24:
                                        time_list[0] -=24
                                subwithtime[i][3] = time_list[0]
                                subwithtime[i][4] = time_list[1]
                                subwithtime[i][5] = time_list[2]
                        elif int(subway_data["arrival_message"]) == 0:  # 진입이라면
                            subwithtime[1][3] = time_list[0]
                            subwithtime[1][4] = time_list[1]
                            subwithtime[1][5] = time_list[2]
                            for i in range(2, len(subwithtime)): # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
                                term_stations = get_stations_between(subway_data["line_num"], base_sub_list[i-1], base_sub_list[i], int(subway_data["direction"]))
                                for j in range(len(term_stations)-1):
                                    term_time = get_operation_time_by_station_and_line(term_stations[j], ln)
                                    if term_time is not None: #역간시간정보 있으면
                                        mins,secs,trash = map(int, term_time.split(":"))
                                        term_min += mins
                                        term_sec += secs
                                    else: #역간시간정보 없으면
                                        pass
                                time_list[1] += term_min
                                time_list[2] += term_sec
                                time_list[2] += 30 # 정차시간
                                while(time_list[2]>=60):
                                    time_list[2] -= 60
                                    time_list[1] += 1
                                    if time_list[1]>=60:
                                        time_list[1] -= 60
                                        time_list[0] += 1
                                        if time_list[0]>=24:
                                            time_list[0] -=24
                                while(time_list[1]>=60):
                                    time_list[1] -= 60
                                    time_list[0] += 1
                                    if time_list[0]>=24:
                                        time_list[0] -=24
                                subwithtime[i][3] = time_list[0]
                                subwithtime[i][4] = time_list[1]
                                subwithtime[i][5] = time_list[2]

            #응답 데이터 구성
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
