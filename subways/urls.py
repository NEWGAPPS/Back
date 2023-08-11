from django.urls import path
from .views import SubwayListView

urlpatterns = [
    path('subways/', SubwayListView.as_view(), name='subway-list'),
]
