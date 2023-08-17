import requests, json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from .models import Subway
from .serializers import SubwaySerializer
from .subs import Normal, nametonum
from collections import OrderedDict

REALTIME_API_KEY = settings.REALTIME_API_KEY

start_index = 0
end_index = 10

class SubwayListView(APIView):
    def get(self, request, *args, **kwargs):

        # 요청을 보낼 locations 앱의 API 엔드포인트 URL
        Curlat = float(kwargs["Curlat"])
        Curlng = float(kwargs["Curlng"])

        locations_url = "http://127.0.0.1:8000/api/locations?lat={}&lng={}".format(Curlat, Curlng)

        
        print(Curlat, Curlng)
        try:
            sbw_response = requests.get(locations_url)
            sbw_data = sbw_response.json()
            sbw = sbw_data["result_data"]
        except json.JSONDecodeError as e:
            sbw = {}  # 빈 딕셔너리로 초기화하여 에러 처리
        
        result_data = []

        for subway_nm, station_names in sbw.items():
            if station_names:  # 비어있지 않은 경우에만 검색 수행
                station_data = {}
                
                idx_list = [Normal[subway_nm].index(station) for station in station_names]
                min_idx = min(idx_list)

                adjacent_indices = range(min_idx - 1, min_idx + 3)
                adjacent_stations = [Normal[subway_nm][i] for i in adjacent_indices if 0 <= i < len(Normal[subway_nm])]
            
                # 인접한 역의 개수가 4개가 아니면 마지막 4개 역을 선택
                if len(adjacent_stations) != 4:
                    adjacent_stations = Normal[subway_nm][-4:]
        
                trains = []

                print(adjacent_stations)

                url = f"http://swopenAPI.seoul.go.kr/api/subway/{REALTIME_API_KEY}/json/realtimePosition/0/10/{subway_nm}"
                response = requests.get(url)
                data = response.json()
                if 'realtimePositionList' in data:
                    realtime_position_list = data['realtimePositionList']

                    for entry in realtime_position_list:
                        if entry['statnNm'] in adjacent_stations:
                            trains.append({
                                "line_num": entry["subwayNm"],
                                "direction": entry["updnLine"],
                                "express": entry["directAt"],
                                "arrival_message": entry["trainSttus"],
                                "cur_station": entry["statnNm"],
                                "endstation": entry["statnTnm"],
                                "msg_time": entry["recptnDt"],
                                "train_num": entry["trainNo"]
                            })

                station_data = {
                    "station_num": subway_nm,
                    "station_list": adjacent_stations,
                    "trains": trains
                }
                result_data.append(station_data)

        return Response({"result_data": result_data})
