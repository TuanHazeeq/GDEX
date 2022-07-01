from django.core.management.base import BaseCommand, CommandError
from trackerfeed.models import Movement
from trackerfeed.management.functions.function_list import list_vehicles_movement
import pandas as pd
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Show vehicles that has moved'

    def add_arguments(self, parser):
        parser.add_argument('-s', type=str, default=datetime.today()- timedelta(days=1), help='Start Date Time Range')
        parser.add_argument('-e', type=str, default=datetime.today(), help='End Date Time Range')
        parser.add_argument('-st', type=int, default=5, help='Stationary Treshold')

    def handle(self, *args, **options):
        movementdf = pd.DataFrame()
        try:
            movementdf = list_vehicles_movement(options['s'], options['e'], options['st'])
        except Exception as e: print(e)

        movementdf.to_csv("list_vehicle_moved.csv", index=False)
