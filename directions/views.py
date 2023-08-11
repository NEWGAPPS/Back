from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests  # requests 라이브러리를 이용하여 API 호출

class SubwayArrivalInfoView(APIView):
    def get(self, request, format=None):
        # Subways 앱의 API 엔드포인트에 요청을 보내서 실시간 데이터 가져오기
        response = requests.get("URL_TO_SUBWAYS_APP_API")  # subways에서 정해준대로
        realtime_data = response.json() if response.status_code == 200 else {}

        # 여기서 필요한 정보를 추출하여 응답 데이터 구성
        previous_station = "이전역"
        next_station = realtime_data.get("next_station", "")
        next_arrival = realtime_data.get("next_arrival", "10분 후")
        next_next_arrival = realtime_data.get("next_next_arrival", "20분 후")
        next_next_next_arrival = realtime_data.get("next_next_next_arrival", "30분 후")

        response_data = {
            "previous_station": previous_station,
            "next_station": next_station,
            "next_arrival": next_arrival,
            "next_next_arrival": next_next_arrival,
            "next_next_next_arrival": next_next_next_arrival,
        }

        return Response(response_data)
    
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
