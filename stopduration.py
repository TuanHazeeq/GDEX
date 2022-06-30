from sqlalchemy import create_engine
import time
import pandas as pd
import geopandas as gpd

#Finding point of vehicles when they are parked
def vehicles_stationary_location(start_dt, end_dt, con):
    df = pd.DataFrame()
    try:
        start_time=time.time()

        sql="""SELECT vehicle_no, a.name as location, odometer, time_stamp
        FROM vtracker_trackerfeed b LEFT JOIN areas a
        ON ST_DWITHIN(ST_TRANSFORM(b.coordinate::geometry,3380), ST_TRANSFORM(a.polygon,3380),100)
        WHERE time_stamp >= \'{}\' AND time_stamp < \'{}\'
        AND ignition = 'false'
        ORDER BY vehicle_no, time_stamp"""
        sql = sql.format(start_dt,end_dt)
        df = pd.read_sql(sql,con)

        df = df.groupby(['vehicle_no','odometer','location'],dropna=False)['time_stamp'].agg(['min','max']).reset_index()
        df['duration'] = df['max']-df['min']
        df = df.drop(['max','min'], axis=1)
        df = df.groupby(['vehicle_no','location'], dropna=False)['duration'].agg('sum').reset_index()
        df['percentage'] = 100 * df['duration'] / df.groupby(['vehicle_no'])['duration'].transform('sum')


        df['location'] = df['location'].fillna('NA')
        df['percentage'] = df['percentage'].round(1)
        df['duration'] = df['duration'] / pd.Timedelta(hours=1)
        df['duration'] = df['duration'].round(2)
        idx = df.groupby(['vehicle_no'])['percentage'].transform(max) == df['percentage']
        df = df[idx].reset_index().drop(['index'], axis=1)

        print("Execution time (highest_duration_stop_point): {}".format(time.time()-start_time))
    except Exception as e: print(e)
    return df

#start execution
start_time = time.time()

#Date range
start_dt = '2022-04-02 0:0:0'
end_dt = '2022-04-03 0:0:0'

#database connection
try:
    db_connection_url = "postgresql://postgres:test1234@localhost:5432/trackerfeed"
    con = create_engine(db_connection_url)
except Exception as e: print(e)

#Call function
list_vehicle_stationary = vehicles_stationary_location(start_dt,end_dt,con)

#Output
print(list_vehicle_stationary)
list_vehicle_stationary.to_csv('list_vehicle_stationary.csv')

print("Execution time (All) : {}".format(time.time()-start_time))