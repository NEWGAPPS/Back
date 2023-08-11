# subways/views.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from .models import Subway
from .serializers import SubwaySerializer


REALTIME_API_KEY = settings.REALTIME_API_KEY

subway_nm = '5호선'
start_index = 0
end_index = 10
selected_statn_ids = [1005000530,1005000529]
selected_statn_ids.sort()
updn_line = '1' #하행

class SubwayListView(APIView):
    def get(self, request, *args, **kwargs):
        # API 호출
        api_url = f'http://swopenAPI.seoul.go.kr/api/subway/{API_KEY}/json/realtimePosition/{start_index}/{end_index}/{subway_nm}'
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json().get('realtimePositionList', [])  # API 응답에서 데이터 추출
            filtered_data = [entry for entry in data if entry['updnLine'] == updn_line]
            # 상행일 경우 가장 큰 역부터 하나씩 줄여가며 4개 역을 탐색, 하행일 경우 가장 작은 역부터 하나씩 키워가며 4개 역을 탐색

            train_ids = []
            if(updn_line==1):
                for entry in filtered_data:
                    for i in range(4):
                        if entry['statnId'] == str(selected_statn_ids[0] + i):
                            train_ids.append(entry['trainNo'])
            else:
                for entry in filtered_data:
                    for i in range(4):
                        target_statn_id = str(selected_statn_ids[0] + i) if updn_line == '1' else str(selected_statn_ids[-1] - i)
                        if entry['statnId'] == target_statn_id:
                            train_ids.append(entry['trainNo'])

            
            return Response(train_ids)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)