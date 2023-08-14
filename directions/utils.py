# import requests
# import copy
# import sys
# from datetime import datetime
# from .models import SubwayStationtime
# #호선별 정보를 저장해보자
# #3 4 7 8 9 #모든건 하행 기준으로 하자

# Normal = {
#     "3호선": ["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"],
#     "4호선": ["진접","오남","별내별가람","당고개","상계","노원", "창동","쌍문","수유","미아","미아사거리","길음","성신여대입구","한성대입구","혜화","동대문","동대문역사문화공원","충무로","명동","회현","서울역","숙대입구","삼각지","신용산","이촌","동작","총신대입구","사당","남테령","선바위","경마공원","대공원","과천","정부과천청사","인덕원","평촌","범계","금정","산본","수리산","대야미","반월","상록수","한대앞","고잔","초지","안산","신길온천","정왕","오이도"],
#     "7호선": ["장암","도봉산","수락산","마들","노원","중계","하계","공릉","태릉입구","먹골","중화","상봉","면목","사가정","용마산","중곡","군자","어린이대공원","건대입구","뚝섬유원지","청담","강남구청","학동","논현","반포","고속터미널","내방","총신대입구","남성","숭실대입구","상도","장승배기","신대방삼거리","보라매","신풍","대림","남구로","가산디지털단지","철산","광명사거리","천왕","온수","까치울","부천종합운동장","춘의","신중동","부천시청","상동","삼산체육관","굴포천","부평구청","산곡","석남"],
#     "8호선": ["암사","천호","강동구청","몽촌토성","잠실","석촌","송파","가락시장","문정","장지","복정","남위례","산성","남한산성입구","단대오거리","신흥","수진","모란"],
#     "9호선": ["개화","김포공항","공항시장","신방화","마곡나루","양천향교","가양","증미","등촌","염창","신목동","선유도","당산","국회의사당","여의도","샛강","노량진","노들","흑석","동작","구반포","신반포","고속터미널","사평","신논현","언주","선정릉","삼성중앙","봉은사","종합운동장","삼전","석촌고분","석촌","송파나루","한성백제","올림픽공원","둔촌오륜","중앙보훈병원"],
# }

# Express = {
#     "4호선" : ["당고개","사당","금정","산본","상록수","중앙","초지","안산","정왕","오이도"],
#     "9호선" : ["김포공항","마곡나루","가양","염창","당산","여의도","노량진","동작","고속터미널","신논현","선정릉","봉은사","종합운동장","석촌","올림픽공원","중앙보훈병원"]
# }

# #Subways로 부터 data 받아오는 함수
# def call_subway_api():
#     url = "URL_TO_SUBWAY_API"  # 실제 API 엔드포인트 URL로 대체해야 합니다.
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # HTTP 요청이 성공적이지 않을 경우 예외를 발생시킵니다.
#         data = response.json()       # JSON 응답 데이터를 파싱하여 딕셔너리로 변환합니다.
        
#         # 데이터를 가공 또는 활용하는 로직을 추가하세요
#         # data를 이용한 작업을 진행하세요
        
#         return data  # 원하는 데이터를 반환합니다.
#     except requests.exceptions.RequestException as e:
#         print("API 요청 중 오류 발생:", e)
#         return None

# #Model로 부터 역간시간 받아오는 함수
# def get_operation_time_by_station_and_line(station_name, line_number):
#     try:
#         subway_data = SubwayStationtime.objects.get(station_name=station_name, line_number=line_number)
#         operation_time = subway_data.operation_time
#         return operation_time
#     except SubwayStationtime.DoesNotExist:
#         return None

# # 함수 호출을 통해 API 데이터를 가져옴
# subway_data = call_subway_api()

# # data 예시
# # subway_data = {
# #         "line_num": "호선", #(subwayNm)
# #         "direction": "상행", #(updnLine) (0 : 상행/내선, 1 : 하행/외선)
# # 	      "express": "급행", #(directAt) (1:급행, 0:아님)
# #         "arrival_message": "도착", #(trainSttus) (0:진입 1:도착, 2:출발, 3:전역출발)
# #         "cur_station": "00역", #(statnNm)
# #         "endstation": "00", #(statnTnm)
# # 		  "msg_time": "2023-08-11 10:51:42" #(recptnDt)
# #         }

# # 받아올 데이터가 있을시에는 (주변에 역이 있을 시에)
# if subway_data is not None:
#     # Subway_line 이라는 일단 호선을 받아옴
#     if subway_data["express"]==0: #완행일때
#         line_num_value = subway_data["line_num"]
#         Subway_line = Normal.get(line_num_value, [])
#     else: #급행일때
#         line_num_value = subway_data["line_num"]
#         Subway_line = Express.get(line_num_value, [])
    
#     # base_sub_list 라는 호선을 deepcopy한 리스트를 작성해서 모두 하행을 통일 시켜줌
#     base_sub_list = copy.deepcopy(Subway_line)
#     if subway_data["direction"] == 0: #상행이면
#         base_sub_list.reverse()
#     else: #하행이면
#         pass

# #여기서부터 도착인지 뭔지에 따라서 list start를 다시 짜야될듯....
# # 0진입: cur==다음역 : list에서 cur station 이전역을 start로 짜되, msg time을 index1로 설정하고 그 뒤부터 time더해주기
# # 1도착: cur==현재역 : list에서 cur station 을 start로 짜되, index 1 = msg time + time 더해줘서 cur 뒤 4개 입력.
# # 2출발: cur==이전역 : list에서 cur station 을 start로 짜되, index 1 = msg time + time 더해줘서 cur 뒤 4개 입력.
# # 3전역 출발: cur==이전역 : list에서 cur station 이전역을 start로 짜되, index 1 = msg time + time 더해줘서 cur 뒤 4개 입력. 
#     # if subway_data["express"]==0: #완행이라면 이라고 판단했지만, 급해 완행 둘다 상관이없음
#     target_element = subway_data["cur_station"]
#     index_of_target = base_sub_list.index(target_element)  # 특정 요소의 인덱스 가져오기
#     if index_of_target>=2: #current역이 첫역이 아니라면
#         if subway_data["arrival_message"]==0 or subway_data["arrival_message"]==3:
#             index_of_target -= 1 #이전역으로 세팅
#             base_sub_list = base_sub_list[index_of_target:] 
#         else:
#             base_sub_list = base_sub_list[index_of_target:]
#     else:
#         #이전역이나 현재역이 첫역이라는 소리이기 때문에 에러 띄우고 종료
#         print("Error")
#         sys.exit(1)

#     #msg_time 저장받아야됨 time_list에.
#     #최종리스트가 subwithtime
#     subwithtime = [[x, -1, -1, -1] for x in base_sub_list] #[0]은 역이름 [1]은 도착시 [2]는 도착분 [3]은 도착초
#     time_str = subway_data["msg_time"]  # "2023-08-11 10:51:42"
#     datetime_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
#     hour = datetime_obj.hour  # 시간
#     minute = datetime_obj.minute  # 분
#     second = datetime_obj.second  # 초
#     time_list = [hour, minute, second]  # 시간, 분, 초를 리스트로 저장
    
#     if subway_data["express"]==0:
#         if subway_data["arrival_message"]!=0: # 진입이 아니라면
#             for i in range(1,5): # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
#                 term_time = get_operation_time_by_station_and_line(base_sub_list[i], subway_data["line_num"])
#                 if term_time is not None: #역간시간정보 있으면
#                     mins,secs = map(int, term_time.split(":"))
#                     time_list[1] += mins
#                     time_list[2] += secs
#                     time_list[2] += 25 #정차시간
#                     if time_list[2] >= 120:
#                         time_list[2] -= 120
#                         time_list[1] += 2
#                     elif time_list[2] >= 60:
#                         time_list[2] -= 60
#                         time_list[1] += 1
#                     if time_list[1] >= 120:
#                         time_list[0] += 2
#                         time_list[1] -= 120
#                     elif time_list[1] >= 60:
#                         time_list[0] += 1
#                         time_list[1] -= 60
#                     if time_list[0] >= 24:
#                         time_list[0] -= 24
#                     subwithtime[i][1] = time_list[0]
#                     subwithtime[i][2] = time_list[1]
#                     subwithtime[i][3] = time_list[2]
#                 else: #역간시간정보 없으면
#                     pass
#         elif subway_data["arrival_message"]==0: # 진입이라면
#             subwithtime[1][1] = time_list[0]
#             subwithtime[1][2] = time_list[1]
#             subwithtime[1][3] = time_list[2]
#             for i in range(2,5): # 근래의 4개의 역중에서 db 존재하는 놈들만 시간더해줘서 시간 입력
#                 term_time = get_operation_time_by_station_and_line(base_sub_list[i], subway_data["line_num"])
#                 if term_time is not None: #역간시간정보 있으면
#                     mins,secs = map(int, term_time.split(":"))
#                     time_list[1] += mins
#                     time_list[2] += secs
#                     time_list[2] += 25 #정차시간
#                     if time_list[2] >= 120:
#                         time_list[2] -= 120
#                         time_list[1] += 2
#                     elif time_list[2] >= 60:
#                         time_list[2] -= 60
#                         time_list[1] += 1
#                     if time_list[1] >= 120:
#                         time_list[0] += 2
#                         time_list[1] -= 120
#                     elif time_list[1] >= 60:
#                         time_list[0] += 1
#                         time_list[1] -= 60
#                     if time_list[0] >= 24:
#                         time_list[0] -= 24
#                     subwithtime[i][1] = time_list[0]
#                     subwithtime[i][2] = time_list[1]
#                     subwithtime[i][3] = time_list[2]
#                 else: #역간시간정보 없으면
#                     pass
#     else: #급행이면
#         pass








# # Normal = {
# #     "1호선_광명행": ["영등포","신도림","구로","가산디지털단지","독산","금천구청","광명"]
# #     "1호선 "
# # }
# # #1호선
# # uplane_one = {
# #     #상행:
# #     "소요산행": ["인천","동인천","도원","제물포","도화","주안","간석","동암","백운","부평","부개","송내","중동","부천","소사","역곡","온수","오류동","개봉","구일","구로","신도림","영등포","신길","대방","노량진","용산","남영","서울역","시청","종각","종로3가","종로5가","동대문","동묘앞","신설동","제기동","청량리","회기","외대앞","신이문","석계","광운대","월계","녹천","창동","방학","도봉","도봉산","망월사","회룡","의정부","가능","녹양","양주","덕계","덕정","지행","동두천중앙","보산","동두천","소요산"],

# # }
# # #상행: 
# # 동두천행(101), 양주행(107), 의정부행(110), 광운대행(119), 청량리행(124), 동묘앞행(127), 서울역행(133), 용산행(135), 영등포행(139), 구로행(141), 병점행(P157), 천안행(P169)



# # 하행: 광운대행(119), 서울역행(133), 구로행(141), 부천행(148), 부평행(152), 동인천행(160), 인천행(161), 광명행(P144-1), 병점행(P157), 서동탄행(P157-1), 천안행(P169), 신창행(P177)





# # 2호선

# # 상행: 외선순환, 을지로입구행(202), 성수행(211), 삼성행(219), 서울대입구행(228), 신도림행(234), 홍대입구행(239)



# # 하행: 내선순환, 을지로입구행(202), 성수행(211), 신설동행(211-4), 삼성행(219), 서울대입구행(228), 신도림행(234), 까치산행(234-4), 홍대입구행(239)





# # # 3호선

# # # 상행: 대화행(309), 구파발행(320), 독립문행(326), 압구정행(336)



# # # 하행: 삼송행(318), 구파발행(320), 약수행(333), 도곡행(344), 수서행(349), 오금행(352)





# # # ​4호선 

# # # ​상행:​ 당고개행(409), 노원행(411), 한성대입구행(419), 사당행(433), 금정행(443), 안산행(453)



# # # 하행:​ 서울역행(426), 사당행(433), 산본행(444), 안산행(453), 오이도행(456)





# # ​5호선 

# # 상행:​ 방화행(510), 화곡행(517), 여의도행(526), 애오개행(530), 왕십리행(540), 군자행(544), 강동행(548)



# # 하행:​ 여의도행(526), 애오개행(530), 왕십리행(540), 군자행(544), 상일동행(553), 하남검단산행(558), 마천행(P555)





# # ​6호선 

# # 상행:​ 응암순환행, 새절행(616), 대흥행(625), 공덕행(626), 한강진행(631), 안암행(639)



# # 하행:​ 응암행(610), 대흥행(625), 공덕행(626), 한강진행(631), 안암행(639), 봉화산행(647), 신내행(648)





# # # ​7호선 

# # # ​상행:​ 장암행(709), 도봉산행(710), 수락산행(711), 태릉입구행(717), 건대입구행(727), 청담행(729), 내방행(735), 신풍행(743), 온수행(750)



# # # 하행:​ 건대입구행(727), 청담행(729), 내방행(735), 신풍행(743), 온수행(750), 부평구청행(759), 석남행(761)





# # # ​8호선 

# # # 상행:​ 암사행(810), 잠실행(814), 가락시장행(817)



# # # ​하행:​ 가락시장행(817), 모란행(827)





# # # ​9호선 

# # # ​상행:​ 개화행(901), 김포공항행(902), 마곡나루행(905), 가양행(907), 염창행(910), 당산행(913), 노량진행(917), 동작행(920), 신논현행(925), 삼전행(931)



# # # 하행:​ 가양행(907), 당산행(913), 동작행(920), 신논현행(925), 삼전행(931), 중앙보훈병원행(938)

# # # ​경의중앙선 

# # # 상행:​ 임진강행(K336), 문산행(K335), 일산행(K326), 대곡행(K322), 수색행(K317), 용산행(K110), 청량리행(K117)



# # # 하행:​ 문산행(K335), 서울역행(P313), 용산행(K110), 청량리행(K117), 덕소행(K126), 용문행(K137), 지평행(K138)

# # # 공항철도 

# # # 상행:​ 서울역행(A01), 디지털미디어시티행(A04)



# # # 하행:​ 검암행(A07), 인천공항2터미널행(A11)

# # ​경춘선 

# # ​상행:​ 청량리행(K117), 광운대행(119), 상봉행(K120), 평내호평행(P128)



# # 하행:​ 평내호평행(P128), 마석행(P130), 춘천행(P140)

# # # 수인분당선 

# # # 상행:​ 청량리행(K209), 왕십리행(K210), 죽전행(K233), 고색행(K246), 오이도행(K258)



# # # 하행:​ 죽전행(K233), 고색행(K246), 오이도행(K258), 인천행(K272)

# # # 신분당선 

# # # 상행:​ 강남행(D07)



# # # 하행:​ 광교경기대행(D19)


# # # 우이신설선 

# # # 상행:​ 북한산우이행(S110)



# # # 하행:​ 신설동행(S122)
