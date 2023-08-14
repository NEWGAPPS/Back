# subways/views.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from .models import Location
from .serializers import LocationSerializer

import json
import os
from math import sqrt

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the JSON file
json_file_path = os.path.join(current_dir, 'coordinate_obj.json')

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)


REALTIME_API_KEY = settings.REALTIME_API_KEY

# curLang = 37.549151
# curLat = 126.944775

curLang = 37.496970
curLat = 127.122720



# sbw = {
#     '7호선': [1007000760, 1007000761],
#     '4호선': [1004000432,1004000433]
# }

def distance(curLang, curLat, lang, lat):

    return sqrt((curLang - lang)**2 + (curLat - lat)**2)

class LocationListView(APIView):
    def get(self, request, *args, **kwargs):


        result_data = []
        error_data = []

        for entry in data:

            try:
                lang = float(entry['coordinate'][0])
                lat = float(entry['coordinate'][1])
                dist = distance(curLang, curLat, lang, lat)

                result_data.append((dist, entry['name']))
            except:
                error_data.append(entry['name'])


        result_data.sort()
            


        

        return Response({"result_data": result_data, "error_data" : error_data})
