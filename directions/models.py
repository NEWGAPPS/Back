from django.db import models

class SubwayStation(models.Model):
    line_number = models.IntegerField()
    station_name = models.CharField(max_length=100)
    eng_name = models.CharField(max_length=100)
    operation_time = models.CharField(max_length=10)
    exit = models.IntegerField()

    def __str__(self):
        return self.station_name
