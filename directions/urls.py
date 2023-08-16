from django.urls import path
from .views import DirectionsAPIView

urlpatterns = [
    path('directions/', DirectionsAPIView.as_view(), name='directions-api'),  # URL을 적절하게 설정하세요
]

# from django.urls import path
# from .views import SubwayAPIView
# urlpatterns = [
#     path("test/", SubwayAPIView.as_view())
# ]