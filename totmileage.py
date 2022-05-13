from sqlalchemy import create_engine
import time
import pandas as pd
import geopandas as gpd

#List all vehicles traveled in all area(polygon)
def vehicles_traveled_in_all_area(start_date,end_date,con):
    try:
        start_time = time.time()
        sql="""WITH temp AS
        (SELECT vehicle_no, a.name,
        (odometer - LAG(odometer, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp DESC)) as mileage
        FROM vtracker_trackerfeed b JOIN areas a ON ST_WITHIN(b.coordinate::geometry, a.polygon)
        WHERE DATE(time_stamp) >= \'{}\' AND DATE(time_stamp) <=\'{}\'
        GROUP BY vehicle_no, a.name, odometer, time_stamp
        ORDER BY vehicle_no)
        SELECT vehicle_no, name, COALESCE(sum(mileage),0) as mileage FROM temp
        GROUP BY vehicle_no, name"""
        sql = sql.format(start_date,end_date)
        df = pd.read_sql(sql,con)
        print("Execution time (vehicles_traveled_in_all_area): {}".format(time.time()-start_time))
        return df
    except Exception as e: print(e)

#Total mileage of vehicles
def tot_mileage(start_date,end_date,con):
    try:
        start_time = time.time()
        sql = """SELECT vehicle_no, MAX(odometer) - MIN(odometer) AS total_mileage
        FROM vtracker_trackerfeed
        WHERE DATE(time_stamp) >= \'{}\' AND DATE(time_stamp) <=\'{}\'
        GROUP BY vehicle_no"""
        sql = sql.format(start_date,end_date)
        df = pd.read_sql(sql,con)
        print("Execution time (tot_mileage): {}".format(time.time()-start_time))
        return df
    except Exception as e: print(e)

#Total mileage of vehicles not within any area (polygon)
def total_mileage_for_other_area(dfarea ,dftotal):
    try:
        start_time = time.time()
        df = dfarea.groupby('vehicle_no').sum().reset_index()
        df = df.merge(dftotal, how='left', on='vehicle_no')
        df['name'] = 'Other'
        df['mileage'] = df['total_mileage']-df['mileage']
        df = df.drop('total_mileage', axis=1)
        print("Execution time (total_mileage_for_other_area): {}".format(time.time()-start_time))
        return df
    except Exception as e: print(e)

#start execution
start_time = time.time()

#Date range
start_date = '2022-04-01'
end_date = '2022-04-30'

#database connection
try:
    db_connection_url = "postgresql://postgres:test1234@localhost:5432/trackerfeed"
    con = create_engine(db_connection_url)
except Exception as e: print(e)

#calling three df function
area = vehicles_traveled_in_all_area(start_date,end_date,con)

total = tot_mileage(start_date,end_date,con)

other = total_mileage_for_other_area(area, total)

#Concat area and other df
result = pd.concat([area,other], ignore_index=True)

#Sort by vehicle_no
result = result.sort_values(by=['vehicle_no','name'], ignore_index=True)

#Merge result df with the total df to include total mileage
result = pd.merge(result, total, how='left', on='vehicle_no')

#Finding percentage of cost distribution
result['percentage'] = result['mileage'] / result['total_mileage']

#Output
print(result)

#Save to percentage.csv
result.to_csv('percentage.csv', index=False)

print("Execution time (All) : {}".format(time.time()-start_time))

