from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import time

#Finding vehicles that has ignition turned on but is not moving
def list_vehicle_idling(start_dt, end_dt, con):
    df = pd.DataFrame()
    try:
        start_time = time.time()
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
        df = pd.read_sql(sql, con)
        print("Execution time (list_vehicles_total_idling): {}".format(time.time()-start_time))
    except Exception as e: print(e)
    return df

#start execution
start_time = time.time()

#Date Range
start_dt = '2022-05-02 0:0:0'
end_dt = '2022-05-03 0:0:0'

#database connection
try:
    db_connection_url = "postgresql://postgres:test1234@localhost:5432/trackerfeed"
    con = create_engine(db_connection_url)
except Exception as e: print(e)

#Calling the function
df = list_vehicle_idling(start_dt, end_dt, con)

#Output
df.to_csv('vehicle_idle.csv', index=False)
df = pd.read_csv('vehicle_idle.csv')
print(df)

print("Execution time (All): {}".format(time.time()-start_time))