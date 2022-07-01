#from sqlalchemy import create_engine
from django.db import connection
import pandas as pd
import time

#Finding whether the vehicle has movement or is stationary in a date range
def list_vehicles_movement(start_dt,end_dt, stationary_treshold):
    df = pd.DataFrame()
    try:
        sql="""SELECT vehicle_no, MAX(odometer) - MIN(odometer) as total_mileage
        FROM gdex.vtracker_trackerfeed
        WHERE time_stamp >= \'{}\' AND time_stamp < \'{}\'
        AND odometer > '0'
        GROUP BY vehicle_no
        HAVING MAX(odometer) - MIN(odometer) > {}"""
        sql = sql.format(start_dt, end_dt,stationary_treshold)
        df = pd.read_sql(sql, connection)
    except Exception as e: print(e)
    return df


#Vehicle that does not have gps vendor and no tracker feed and tracker alert
def no_gps(start_dt,end_dt):
    df = pd.DataFrame()
    try:
        #Read from GPS Tracker Analysis
        df = pd.read_csv("GPS Tracker Analysis.csv")
        df['vehicle_no'] = df['vehicle_no'].str.replace(' ', '')

        #Vehicle_no from trackerfeed
        sqlfeed = """SELECT DISTINCT vehicle_no FROM gdex.vtracker_trackerfeed
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        ORDER BY vehicle_no"""
        sqlfeed = sqlfeed.format(start_dt, end_dt)
        feeddf = pd.read_sql(sqlfeed, connection)

        #Vehicle that has no tracker feed
        feeddf['vehicle_no'] = feeddf['vehicle_no'].str.replace(' ', '')
        df_no_feed = df[df['vehicle_no'].isin(feeddf['vehicle_no']) == False]

        #Vehicle_no from trackeralert
        sqlalert = """SELECT DISTINCT vehicle_no FROM gdex.vtracker_trackeralert
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        ORDER BY vehicle_no"""
        sqlalert = sqlalert.format(start_dt, end_dt)
        alertdf = pd.read_sql(sqlalert, connection)

        #Vehicle that has no tracker alert
        alertdf['vehicle_no'] = alertdf['vehicle_no'].str.replace(' ', '')
        df_no_alert = df[df['vehicle_no'].isin(alertdf['vehicle_no']) == False]

        df = pd.concat([df_no_feed, df_no_alert], ignore_index=True).drop_duplicates(['vehicle_no'])
    except Exception as e: print(e)
    return df

#Vehicle that have GUS GPS vendor but does not have tracker feed or alert
#or vehicle that have null GPS vendor but receive GUS tracker feed or alert
def gus_gps_no_feed(start_dt,end_dt):
    df = pd.DataFrame()
    try:
        #Read from tracker analysis
        df = pd.read_csv("GPS Tracker Analysis.csv")
        df['vehicle_no'] = df['vehicle_no'].str.replace(' ', '')

        #vehicle_no that has no gps vendor
        dfnull = df.loc[df['GPSVendor'].isnull()]

        #Vehicle_no have GUS gps vendor
        df = df.loc[df['GPSVendor']=='GUS']

        #Vehicle_no from trackerfeed
        sqlfeed = """SELECT DISTINCT vehicle_no FROM gdex.vtracker_trackerfeed
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        ORDER BY vehicle_no"""
        sqlfeed = sqlfeed.format(start_dt, end_dt)
        feeddf = pd.read_sql(sqlfeed, connection)

        #Vehicle with GUS GPS that has no tracker feed
        feeddf['vehicle_no'] = feeddf['vehicle_no'].str.replace(' ', '')
        gus_df_no_feed = df[df['vehicle_no'].isin(feeddf['vehicle_no']) == False]

        #Vehicle_no from trackeralert
        sqlalert = """SELECT DISTINCT vehicle_no FROM gdex.vtracker_trackeralert
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        ORDER BY vehicle_no"""
        sqlalert = sqlalert.format(start_dt, end_dt)
        alertdf = pd.read_sql(sqlalert, connection)

        #Vehicle with GUS GPS that has no tracker alert
        alertdf['vehicle_no'] = alertdf['vehicle_no'].str.replace(' ', '')
        gus_df_no_alert = df[df['vehicle_no'].isin(alertdf['vehicle_no']) == False]

        df = pd.concat([gus_df_no_feed, gus_df_no_alert], ignore_index=True).drop_duplicates(['vehicle_no'])

        #Vehicle_no that has gus vendor id from trackerfeed
        sqlnullfeed = """SELECT DISTINCT vehicle_no FROM gdex.vtracker_trackerfeed
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        AND vendor = 1
        ORDER BY vehicle_no"""
        sqlnullfeed = sqlnullfeed.format(start_dt, end_dt)
        nullfeeddf = pd.read_sql(sqlnullfeed, connection)

        #Check if any null gps vendor have tracker feed from gus vendor
        nullfeeddf['vehicle_no'] = nullfeeddf['vehicle_no'].str.replace(' ', '')
        null_gps_df_feed = pd.merge(dfnull,nullfeeddf, on='vehicle_no')

        #Vehicle_no that has gus vendor id from trackeralert
        sqlnullalert = """SELECT DISTINCT vehicle_no FROM gdex.vtracker_trackeralert
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        AND vendor = 1
        ORDER BY vehicle_no"""
        sqlnullalert = sqlnullalert.format(start_dt, end_dt)
        alertnulldf = pd.read_sql(sqlnullalert, connection)

        #Check if any null gps vendor have tracker alert from gus vendor
        alertnulldf['vehicle_no'] = alertnulldf['vehicle_no'].str.replace(' ', '')
        null_gps_df_alert = pd.merge(dfnull,alertnulldf, on='vehicle_no')

        dfnull = pd.concat([null_gps_df_feed, null_gps_df_alert], ignore_index=True).drop_duplicates(['vehicle_no'])

        df = pd.concat([df, dfnull], ignore_index=True)
    except Exception as e: print(e)
    return df

#Vehicle that have i-TRACK GPS vendor but does not have tracker feed or alert
#or vehicle that have null GPS vendor but receive i-TRACK tracker feed or alert
def itrack_gps_no_feed(start_dt,end_dt):
    df = pd.DataFrame()
    try:
        #Read from tracker analysis
        df = pd.read_csv("GPS Tracker Analysis.csv")
        df['vehicle_no'] = df['vehicle_no'].str.replace(' ', '')

        #vehicle_no that has no gps vendor
        dfnull = df.loc[df['GPSVendor'].isnull()]

        #Vehicle_no have i-TRACK gps vendor
        df = df.loc[df['GPSVendor']=='i-TRACK']

        #Vehicle_no from trackerfeed
        sqlfeed = """SELECT DISTINCT vehicle_no FROM gdex.vtracker_trackerfeed
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        ORDER BY vehicle_no"""
        sqlfeed = sqlfeed.format(start_dt, end_dt)
        feeddf = pd.read_sql(sqlfeed, connection)

        #Vehicle with i-TRACK GPS that has no tracker feed
        feeddf['vehicle_no'] = feeddf['vehicle_no'].str.replace(' ', '')
        itrack_df_no_feed = df[df['vehicle_no'].isin(feeddf['vehicle_no']) == False]

        #Vehicle_no from trackeralert
        sqlalert = """SELECT DISTINCT vehicle_no FROM gdex.vtracker_trackeralert
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        ORDER BY vehicle_no"""
        sqlalert = sqlalert.format(start_dt, end_dt)
        alertdf = pd.read_sql(sqlalert, connection)

        #Vehicle with i-TRACK GPS that has no tracker alert
        alertdf['vehicle_no'] = alertdf['vehicle_no'].str.replace(' ', '')
        itrack_df_no_alert = df[df['vehicle_no'].isin(alertdf['vehicle_no']) == False]

        df = pd.concat([itrack_df_no_feed, itrack_df_no_alert], ignore_index=True).drop_duplicates(['vehicle_no'])

        #Vehicle_no that has itrack vendor id from trackerfeed
        sqlnullfeed = """SELECT DISTINCT vehicle_no FROM gdex.vtracker_trackerfeed
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        AND vendor = 2
        ORDER BY vehicle_no"""
        sqlnullfeed = sqlnullfeed.format(start_dt, end_dt)
        nullfeeddf = pd.read_sql(sqlnullfeed, connection)

        #Check if any null gps vendor have tracker feed from itrack vendor
        nullfeeddf['vehicle_no'] = nullfeeddf['vehicle_no'].str.replace(' ', '')
        null_gps_df_feed = pd.merge(dfnull,nullfeeddf, on='vehicle_no')

        #Vehicle_no that has itrack vendor id from trackeralert
        sqlnullalert = """SELECT DISTINCT vehicle_no FROM gdex.vtracker_trackeralert
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        AND vendor = 2
        ORDER BY vehicle_no"""
        sqlnullalert = sqlnullalert.format(start_dt, end_dt)
        alertnulldf = pd.read_sql(sqlnullalert, connection)

        #Check if any null gps vendor have tracker alert from itrack vendor
        alertnulldf['vehicle_no'] = alertnulldf['vehicle_no'].str.replace(' ', '')
        null_gps_df_alert = pd.merge(dfnull,alertnulldf, on='vehicle_no')

        dfnull = pd.concat([null_gps_df_feed, null_gps_df_alert], ignore_index=True).drop_duplicates(['vehicle_no'])

        df = pd.concat([df, dfnull], ignore_index=True)

    except Exception as e: print(e)
    return df

#Finding vehicle idling duration and idling count and categorizing it by the idling duration
def vehicles_idling_by_duration(start_dt, end_dt):
    df = pd.DataFrame()
    try:
        start_time = time.time()
        #List of vehicle_no with idling time
        sql="""WITH temp AS
        (SELECT vehicle_no,
        odometer, LAG(odometer, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_odometer,
        time_stamp, LAG(time_stamp, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_time_stamp,
        alert_type, LAG(alert_type, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_alert,
        location
        FROM gdex.vtracker_trackeralert
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        ORDER BY vehicle_no, time_stamp)
        SELECT vehicle_no,
        to_char(time_stamp, 'YYYY-MM-DD HH24:MI:SS') AS from,to_char(next_time_stamp, 'YYYY-MM-DD HH24:MI:SS') AS to,
        ROUND(EXTRACT(EPOCH FROM next_time_stamp - time_stamp)/60, 2) AS duration, location FROM temp
        WHERE alert_type = 8 AND next_alert = 7
        AND odometer = next_odometer"""
        sql = sql.format(start_dt, end_dt)
        df = pd.read_sql(sql, connection)

        #vehicle_no idle count and duration with idle duration less than five minutes
        dflessfive = df[df['duration']<5]
        dflessfive = dflessfive.groupby('vehicle_no')['duration'].agg(['count','sum']).reset_index()
        dflessfive.rename(columns= {'sum':'duration <5','count':'<5'}, inplace = True)

        #vehicle_no idle count and duration with idle duration more than five minutes but less than ten minutes
        dflessten = df[(df['duration']>=5) & (df['duration']<10)]
        dflessten = dflessten.groupby('vehicle_no')['duration'].agg(['count','sum']).reset_index()
        dflessten.rename(columns= {'sum':'duration >=5 and <10','count':'>=5 and <10'}, inplace = True)

        #vehicle_no idle count and duration with idle duration more than ten minutes
        dfmoreten = df[df['duration']>=10]
        dfmoreten = dfmoreten.groupby('vehicle_no')['duration'].agg(['count','sum']).reset_index()
        dfmoreten.rename(columns= {'sum':'duration >=10','count':'>=10'}, inplace = True)

        df = pd.merge(dflessfive,dflessten, on='vehicle_no', how='outer')
        df = pd.merge(df, dfmoreten, on='vehicle_no', how='outer')
        df = df.fillna(0)
        df['total_idle_count'] = df['<5']+df['>=5 and <10']+df['>=10']
        df['total_idle_duration'] = df['duration <5']+df['duration >=5 and <10']+df['duration >=10']

        print("Execution time (vehicles_idling_by_duration): {}".format(time.time()-start_time))
    except Exception as e: print(e)
    return df

#List vehicles that has ignition turned on but is not moving(idling)
def list_vehicle_idling(start_dt, end_dt):
    df = pd.DataFrame()
    try:
        start_time = time.time()
        sql="""WITH temp AS
        (SELECT vehicle_no,
        odometer, LAG(odometer, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_odometer,
        time_stamp, LAG(time_stamp, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_time_stamp,
        alert_type, LAG(alert_type, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_alert,
        location, coordinate
        FROM gdex.vtracker_trackeralert
        WHERE time_stamp >= '{}' AND time_stamp < '{}'
        ORDER BY vehicle_no, time_stamp)
        SELECT vehicle_no,
        to_char(time_stamp, 'YYYY-MM-DD HH24:MI:SS') AS from,to_char(next_time_stamp, 'YYYY-MM-DD HH24:MI:SS') AS to,
        ROUND(EXTRACT(EPOCH FROM next_time_stamp - time_stamp)/60, 2) AS duration, location, coordinate FROM temp
        WHERE alert_type = 8 AND next_alert = 7
        AND odometer = next_odometer"""
        sql = sql.format(start_dt, end_dt)
        df = pd.read_sql(sql, connection)
        print("Execution time (list_vehicles_total_idling): {}".format(time.time()-start_time))
    except Exception as e: print(e)
    return df