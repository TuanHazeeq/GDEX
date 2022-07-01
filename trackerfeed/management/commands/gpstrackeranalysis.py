from django.core.management.base import BaseCommand, CommandError
from trackerfeed.management.functions.function_list import gus_gps_no_feed
from trackerfeed.management.functions.function_list import no_gps
from trackerfeed.management.functions.function_list import itrack_gps_no_feed
import pandas as pd
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Show vehicle that has GUS GPS vendor but has no GPS feed'

    def add_arguments(self, parser):
        parser.add_argument('-s', type=str, default=datetime.today()- timedelta(days=30), help='Start Date Time Range')
        parser.add_argument('-e', type=str, default=datetime.today(), help='End Date Time Range')

    def handle(self, *args, **options):
        gus_GPS_df = pd.DataFrame()
        try:
            gus_GPS_df = gus_gps_no_feed(options['s'], options['e'])
            gus_GPS_df = gus_GPS_df.sort_values('Type')
        except Exception as e: print(e)

        itrack_GPS_df = pd.DataFrame()
        try:
            itrack_GPS_df = itrack_gps_no_feed(options['s'], options['e'])
            itrack_GPS_df = itrack_GPS_df.sort_values('Type')
        except Exception as e: print(e)

        noGPSdf = pd.DataFrame()
        try:
            noGPSdf = no_gps(options['s'], options['e'])
            noGPSdf = noGPSdf[ noGPSdf['vehicle_no'].isin(gus_GPS_df['vehicle_no'])== False ]
            noGPSdf = noGPSdf[ noGPSdf['vehicle_no'].isin(itrack_GPS_df['vehicle_no'])== False ]
            noGPSdf = noGPSdf.sort_values('Type')
        except Exception as e: print(e)

        with pd.ExcelWriter('GPS_TRACKER_ANALYSIS.xlsx') as writer:
            gus_GPS_df.to_excel(writer,sheet_name='GUS', index=False)
            itrack_GPS_df.to_excel(writer,sheet_name='i-TRACK', index=False)
            noGPSdf.to_excel(writer,sheet_name='NO_GPS', index=False)