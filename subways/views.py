import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from .models import Subway
from .serializers import SubwaySerializer
from .subs import Normal, nametonum
from collections import OrderedDict

REALTIME_API_KEY = settings.REALTIME_API_KEY

sbw = {
    '7호선': ["산곡", "석남"],
    '4호선': ["고잔", "중앙"],
    '신분당선': ["광교"]
}

start_index = 0
end_index = 50

class SubwayListView(APIView):
    def get(self, request, *args, **kwargs):

        result_data = {}

        for subway_nm, station_names in sbw.items():
            first_station = station_names[0]  # 첫번째 역을 선택
            if len(station_names)>=2 :
                second_station = station_names[-1]
            if first_station in Normal.get(subway_nm, []):
                idx = Normal[subway_nm].index(first_station)

                if idx>=1 and Normal[subway_nm][idx-1]== second_station:
                    idx = Normal[subway_nm].index(second_station)

                adjacent_indices = range(idx - 1, idx + 3)
                adjacent_stations = [Normal[subway_nm][i] for i in adjacent_indices if 0 <= i < len(Normal[subway_nm])]
        
        # 인접한 역의 개수가 4개가 아니면 마지막 4개 역을 선택
                if len(adjacent_stations) != 4:
                    adjacent_stations = Normal[subway_nm][-4:]
        
                result_data[subway_nm] = {
                    "station_list": adjacent_stations,
                    "trains": []
                }

            
            url = f"http://swopenAPI.seoul.go.kr/api/subway/{REALTIME_API_KEY}/json/realtimePosition/0/10/{subway_nm}"
            response = requests.get(url)
            data = response.json()
            if 'realtimePositionList' in data:
                realtime_position_list = data['realtimePositionList']

                for entry in realtime_position_list:
                    if entry['statnNm'] in result_data[subway_nm]["station_list"]:
                        direction = "상행" if entry['updnLine'] == '0' else "하행"
                        result_data[subway_nm]["trains"].append({
                            "line_num": entry["subwayNm"],
                            "direction": direction,
                            "express": entry["directAt"],
                            "arrival_message": entry["trainSttus"],
                            "cur_station": entry["statnNm"],
                            "endstation": entry["statnTnm"],
                            "msg_time": entry["recptnDt"]
                        })

        return Response({"result_data": result_data})
