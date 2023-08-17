from django.urls import path
from .views import SubwayListView

urlpatterns = [
    path('subways/<str:Curlat>/<str:Curlng>', SubwayListView.as_view(), name='subway-list'),
]

#Curlat Curlng