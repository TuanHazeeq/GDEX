from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import time

#Finding whether the vehicle has movement or is stationary in a date range
def list_vehicles_moved(start_dt,end_dt, stationary_treshold, con):
    df = pd.DataFrame()
    try:
        start_time = time.time()
        sql="""SELECT vehicle_no, MAX(odometer) - MIN(odometer) as total_mileage
        FROM gdex.vtracker_trackerfeed
        WHERE time_stamp >= \'{}\' AND time_stamp < \'{}\'
        GROUP BY vehicle_no
        HAVING MAX(odometer) - MIN(odometer) > {}
        ORDER BY vehicle_no"""
        sql = sql.format(start_dt, end_dt,stationary_treshold)
        df = pd.read_sql(sql, con)
        print("Execution time (list_vehicles_moved): {}".format(time.time()-start_time))
    except Exception as e: print(e)
    return df

#start execution
start_time = time.time()

#Date Range
start_dt = '2022-04-02 0:0:0'
end_dt = '2022-04-03 0:0:0'

#This threshold shows how many miles needed for the vehicle to be considered moving
stationary_treshold = 5

#database connection
try:
    db_connection_url = "postgresql://postgres:test1234@localhost:5432/trackerfeed"
    con = create_engine(db_connection_url)
except Exception as e: print(e)

#Calling the function
df = list_vehicles_moved(start_dt, end_dt, stationary_treshold, con)

#Output
df.to_csv('list_vehicles_moved.csv', index=False)
df = pd.read_csv('list_vehicles_moved.csv')
print(df)

print("Execution time (All): {}".format(time.time()-start_time))