from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import time

#Finding whether the vehicle has movement or is stationary in a date range
def totmileage(start_date, end_date, con):
    try:
        sql="""WITH tempTable AS(
            SELECT vehicle_no, DATE(time_stamp),
            (odometer - LAG(odometer, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp DESC)) as mileage
            FROM vtracker_trackerfeed
            WHERE DATE(time_stamp) >= \'{}\' AND DATE(time_stamp) <= \'{}\'
            GROUP BY vehicle_no, time_stamp,odometer, coordinate, id
            ORDER BY vehicle_no, time_stamp DESC
        )
        SELECT date, vehicle_no, sum(mileage) as totmileage,
        CASE WHEN sum(mileage) ISNULL THEN 'Station'
        WHEN sum(mileage) < 0 THEN 'Invalid'
        WHEN sum(mileage) < 10 THEN 'Station'
        ELSE 'Moved'
        END AS movement
        FROM tempTable
        GROUP BY date, vehicle_no
        ORDER BY date, vehicle_no"""
        sql = sql.format(start_date, end_date)
        df = pd.read_sql(sql, con)
        return df
    except Exception as e: print(e)

#start execution
start_time = time.time()

#Date Range
start_date = '2022-04-01'
end_date = '2022-04-30'

#database connection
try:
    db_connection_url = "postgresql://postgres:test1234@localhost:5432/trackerfeed"
    con = create_engine(db_connection_url)
except Exception as e: print(e)

#Calling the function
df = totmileage(start_date, end_date, con)

#Output
df.to_csv('movement.csv', index=False)
df = pd.read_csv('movement.csv')
print(df)