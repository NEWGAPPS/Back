# subways/views.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from .models import Subway
from .serializers import SubwaySerializer


REALTIME_API_KEY = settings.REALTIME_API_KEY

sbw = {
    '7호선': [1007000760, 1007000761],
    '4호선': [1004000432,1004000433]
}

start_index = 0
end_index = 10

class SubwayListView(APIView):
    def get(self, request, *args, **kwargs):

        
        result_data = []

        for subway_nm, selected_statn_ids in sbw.items():

            url = f"http://swopenAPI.seoul.go.kr/api/subway/{REALTIME_API_KEY}/json/realtimePosition/0/10/{subway_nm}"
            response = requests.get(url)
            data = response.json()
            if 'realtimePositionList' in data:
                realtime_position_list = data['realtimePositionList']

                for entry in realtime_position_list:
                    if entry['updnLine'] == '0':
                        for i in range(-1, 3):
                                adjacent_statn_id = selected_statn_ids[0] + i
                                if entry['statnId'] == str(adjacent_statn_id):
                                    result_data.append({
                                        "line_num": entry["subwayNm"],
                                        "direction": "상행",
                                        "express": entry["directAt"],
                                        "arrival_message": entry["trainSttus"],
                                        "cur_station": entry["statnNm"],
                                        "endstation": entry["statnTnm"],
                                        "msg_time": entry["recptnDt"]
                                    })
                    elif entry['updnLine'] == '1':
                        # Check for adjacent statnIds
                        for i in range(-1, 3):
                                adjacent_statn_id = selected_statn_ids[0] + i
                                if entry['statnId'] == str(adjacent_statn_id):
                                    result_data.append({
                                        "line_num": entry["subwayNm"],
                                        "direction": "하행",
                                        "express": entry["directAt"],
                                        "arrival_message": entry["trainSttus"],
                                        "cur_station": entry["statnNm"],
                                        "endstation": entry["statnTnm"],
                                        "msg_time": entry["recptnDt"]
                                    })


                    
            

        return Response({"result_data": result_data})