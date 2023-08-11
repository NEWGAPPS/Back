from django.db import models

class SubwayStationtime(models.Model):
    serial_number = models.IntegerField()
    line_number = models.IntegerField()
    station_name = models.CharField(max_length=100)
    operation_time = models.CharField(max_length=10)
    distance_between_stations = models.FloatField()
    cumulative_distance = models.FloatField()

    def __str__(self):
        return self.station_name