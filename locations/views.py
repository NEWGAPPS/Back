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
import requests
import xml.etree.ElementTree as ET

url = "http://swopenAPI.seoul.go.kr/api/subway/4f4b6c416331303035316e6b4c6d4a/xml/realtimeStationArrival/0/5/서울"


from math import sqrt

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the JSON file
json_file_path = os.path.join(current_dir, 'coordinate_obj.json')

with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)


name2Id_path = os.path.join(current_dir, 'name2Id.json')

with open(name2Id_path, 'r', encoding='utf-8') as json_file:
    name2Id = json.load(json_file)



REALTIME_API_KEY = settings.REALTIME_API_KEY

# curLang = 37.549151
# curLat = 126.944775

# curLang = 37.496970
# curLat = 127.122720



# sbw = {
#     '7호선': [1007000760, 1007000761],
#     '4호선': [1004000432,1004000433]
# }

def distance(curLang, curLat, lang, lat):

    return sqrt((curLang - lang)**2 + (curLat - lat)**2)

class LocationListView(APIView):
    def get(self, request, *args, **kwargs):

        curLng = float(self.request.query_params.get('lng'))
        curLat = float(self.request.query_params.get('lat'))

        print(curLat, curLng)


        sortedNeighbors = []
        result_data = {
            '3호선'  : [],
            '4호선'  : [],
            '7호선'  : [],
            '8호선'  : [],
            '9호선'  : [],
            '신분당선': []
            }
        error_data = []

        for entry in data:

            try:
                lat = float(entry['coordinate'][0])
                lng = float(entry['coordinate'][1])
                dist = distance(curLng, curLat, lng, lat)

                sortedNeighbors.append((dist, entry['name']))
            except:
                error_data.append(entry['name'])


        sortedNeighbors.sort()


        for neighbor in sortedNeighbors[:5]:

            try:
                stationName = neighbor[1]
                

                statnIds = name2Id[stationName]


                for statnId in statnIds:

                    curSubwayNum = statnId[:4]
                    print(curSubwayNum)

                    ## 3호선
                    if curSubwayNum == '1003':
                        ##result_data['3호선'].append(statnId)
                        result_data['3호선'].append(stationName)
                    
                    ## 4호선
                    elif curSubwayNum == '1004':
                        ##result_data['4호선'].append(statnId)
                        result_data['4호선'].append(stationName)
                    
                    ## 7호선
                    elif curSubwayNum == '1007':
                        ##result_data['7호선'].append(statnId)
                        result_data['7호선'].append(stationName)
                    
                    ## 8호선
                    elif curSubwayNum == '1008':
                        ##result_data['8호선'].append(statnId)
                        result_data['8호선'].append(stationName)
                    
                    ## 9호선
                    elif curSubwayNum == '1009':
                        ##result_data['9호선'].append(statnId)
                        result_data['9호선'].append(stationName)

                    ##신분당선
                    elif curSubwayNum == '1077':
                        ##result_data['신분당선'].append(statnId)
                        result_data['신분당선'].append(stationName)

            except:
                error_data.append(entry['name'])

        # trainInfo = {}
        # errorTrain = []

        # for entry in data:

        #     try:
        #         url = "http://swopenAPI.seoul.go.kr/api/subway/477966644873736839364966597454/xml/realtimeStationArrival/0/5/"+entry['name']

        #         response = requests.get(url)
        #         tree = ET.ElementTree(ET.fromstring(response.content))

        #         # Find all statnId elements and extract their values into a list
        #         statn_id_list = set([elem.text for elem in tree.iter("statnId")])


        #         trainInfo[entry['name']] = statn_id_list

        #     except:
        #         errorTrain.append(entry['name'])
            


        

        return Response({"result_data": result_data, "error_data" : error_data})
        #return Response({"trainInfo": trainInfo, 'errorTrain' : errorTrain})
