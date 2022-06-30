from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import time

#Finding vehicles that is parked but the ignition is on
def park_ignition_on(start_dt, end_dt, con):
    df = pd.DataFrame()
    try:
        start_time = time.time()
        sql="""WITH temp AS(
            SELECT vehicle_no,
            LAG(odometer, 1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS previous_odometer,
            odometer AS current_odometer, LAG(odometer, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_odometer,
            time_stamp AS current_time_stamp,
            LAG(time_stamp, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_time_stamp,
            LAG(alert_type, 1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS previous_alert,
            alert_type AS current_alert, LAG(alert_type, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_alert
            FROM gdex.vtracker_trackeralert
            WHERE time_stamp >= \'{}\' AND time_stamp < \'{}\'
            ORDER BY vehicle_no, time_stamp
        )
        SELECT vehicle_no,
        ROUND(EXTRACT(EPOCH FROM next_time_stamp - current_time_stamp)/60, 2) AS duration
        FROM temp
        WHERE previous_alert = 7 AND current_alert = 8 AND next_alert = 7
        AND previous_odometer = current_odometer AND current_odometer = next_odometer"""
        sql = sql.format(start_dt, end_dt)
        df = pd.read_sql(sql, con)

        dflessfive = df[df['duration']<5]
        dflessfive = dflessfive.groupby('vehicle_no')['duration'].agg(['count','sum']).reset_index()
        dflessfive.rename(columns= {'sum':'duration <5','count':'<5'}, inplace = True)

        dflessten = df[(df['duration']>=5) & (df['duration']<10)]
        dflessten = dflessten.groupby('vehicle_no')['duration'].agg(['count','sum']).reset_index()
        dflessten.rename(columns= {'sum':'duration >=5 and <10','count':'>=5 and <10'}, inplace = True)

        dfmoreten = df[df['duration']>=10]
        dfmoreten = dfmoreten.groupby('vehicle_no')['duration'].agg(['count','sum']).reset_index()
        dfmoreten.rename(columns= {'sum':'duration >=10','count':'>=10'}, inplace = True)

        df = pd.merge(dflessfive,dflessten, on='vehicle_no', how='outer')
        df = pd.merge(df, dfmoreten, on='vehicle_no', how='outer')
        df = df.fillna(0)
        df['total_idle_count'] = df['<5']+df['>=5 and <10']+df['>=10']
        df['total_idle_duration'] = df['duration <5']+df['duration >=5 and <10']+df['duration >=10']

        print("Execution time (park_ignition_on): {}".format(time.time()-start_time))
    except Exception as e: print(e)
    return df

#start execution
start_time = time.time()

#Date Range
start_dt = '2022-04-04 0:0:0'
end_dt = '2022-04-05 0:0:0'

#database connection
try:
    db_connection_url = "postgresql://postgres:test1234@localhost:5432/trackerfeed"
    con = create_engine(db_connection_url)
except Exception as e: print(e)

#Calling the function
df = park_ignition_on(start_dt, end_dt, con)

#Output
df.to_csv('park_ignition_on.csv', index=False)
df = pd.read_csv('park_ignition_on.csv')
print(df)

print("Execution time (All): {}".format(time.time()-start_time))