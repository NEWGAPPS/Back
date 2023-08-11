from django.urls import path
from .views import SubwayArrivalInfoView  # 지하철 도착 정보를 처리하는 뷰를 import

urlpatterns = [
    # 다른 URL 패턴들
    path('api/subway-arrival-info/', SubwayArrivalInfoView.as_view(), name='subway-arrival-info'),
]

# from django.urls import path
# from .views import SubwayAPIView
# urlpatterns = [
#     path("test/", SubwayAPIView.as_view())
# ]