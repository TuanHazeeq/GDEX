from django.core.management.base import BaseCommand, CommandError
from trackerfeed.management.functions.function_list import vehicles_idling_by_duration
import pandas as pd
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Show vehicles that has ignition on but is not moving'

    def add_arguments(self, parser):
        parser.add_argument('-s', type=str, default=datetime.today()- timedelta(days=1), help='Start Date Time Range')
        parser.add_argument('-e', type=str, default=datetime.today(), help='End Date Time Range')

    def handle(self, *args, **options):
        idledf = pd.DataFrame()
        try:
            idledf = vehicles_idling_by_duration(options['s'], options['e'])
        except Exception as e: print(e)

        idledf.to_csv("vehicles_idling_by_duration.csv", index=False)
