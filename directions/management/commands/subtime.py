import csv
from django.core.management.base import BaseCommand
from directions.models import SubwayStationtime

class Command(BaseCommand):
    help = 'Import subway station data from CSV'

    def handle(self, *args, **options):
        csv_file_path = 'directions/management/commands/betweentime.csv'  # CSV 파일 경로를 지정하세요

        with open(csv_file_path, 'r', encoding='cp949') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row

            for row in csv_reader:
                station = SubwayStationtime(
                    serial_number=row[0],
                    line_number=row[1],
                    station_name=row[2],
                    operation_time=row[3],
                    distance_between_stations=row[4],
                    cumulative_distance=row[5]
                )
                station.save()

        self.stdout.write(self.style.SUCCESS('Subway station data imported successfully.'))
