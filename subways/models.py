from django.db import models

class Subway(models.Model):
    subwayId = models.CharField(max_length=10)  # 지하철호선ID (문자열로 저장)
    subwayNm = models.CharField(max_length=50)  # 지하철호선명
    statnId = models.CharField(max_length=10)  # 지하철역ID (문자열로 저장)
    statnNm = models.CharField(max_length=50)  # 지하철역명
    trainNo = models.CharField(max_length=10)  # 열차번호
    lastRecptnDt = models.DateTimeField()  # 최종수신날짜 및 시간
    recptnDt = models.DateTimeField()  # 최종수신시간
    updnLine = models.IntegerField()  # 상하행선구분
    statnTid = models.CharField(max_length=10)  # 종착지하철역ID (문자열로 저장)
    statnTnm = models.CharField(max_length=50)  # 종착지하철역명
    trainSttus = models.IntegerField()  # 열차상태구분
    directAt = models.IntegerField()  # 급행여부
    lstcarAt = models.IntegerField()  # 막차여부

    def __str__(self):
        return self.trainNo
