from sqlalchemy import create_engine
import time
import pandas as pd
import geopandas as gpd

#List all vehicles traveled in all area(polygon)
def vehicle_traveled_in_all_area(start_dt,end_dt,con):
    df = pd.DataFrame()
    try:
        start_time = time.time()
        sql="""WITH temp AS
        (SELECT vehicle_no, a.name,
        (odometer - LAG(odometer, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp DESC)) as mileage
        FROM vtracker_trackerfeed b JOIN areas a ON ST_WITHIN(b.coordinate::geometry, a.polygon)
        WHERE time_stamp >= \'{}\' AND time_stamp < \'{}\'
        GROUP BY vehicle_no, a.name, odometer, time_stamp
        ORDER BY vehicle_no)
        SELECT vehicle_no, name, COALESCE(sum(mileage),0) as mileage FROM temp
        GROUP BY vehicle_no, name"""
        sql = sql.format(start_dt,end_dt)
        df = pd.read_sql(sql,con)
        print("Execution time (vehicle_traveled_in_all_area): {}".format(time.time()-start_time))
    except Exception as e: print(e)
    return df

#Total mileage of all vehicles
def total_mileage(start_dt,end_dt,con):
    df = pd.DataFrame()
    try:
        start_time = time.time()
        sql = """SELECT vehicle_no, MAX(odometer) - MIN(odometer) AS total_mileage
        FROM vtracker_trackerfeed
        WHERE time_stamp >= \'{}\' AND time_stamp <\'{}\'
        GROUP BY vehicle_no"""
        sql = sql.format(start_dt,end_dt)
        df = pd.read_sql(sql,con)
        print("Execution time (total_mileage): {}".format(time.time()-start_time))
    except Exception as e: print(e)
    return df

#Total mileage of all vehicles not within any area (polygon) and vehicle mileage percentage in all area
def vehicle_mileage_percentage_in_all_area(dfarea ,dftotal):
    dfresult = pd.DataFrame()
    try:
        start_time = time.time()
        df = dfarea.groupby('vehicle_no').sum().reset_index()
        df = df.merge(dftotal, how='left', on='vehicle_no')
        df['name'] = 'Other'
        df['mileage'] = df['total_mileage']-df['mileage']
        df = df.drop('total_mileage', axis=1)


        #Concat df area and df other
        dfresult = pd.concat([dfarea,df], ignore_index=True)

        #Sort by vehicle_no
        dfresult = dfresult.sort_values(by=['vehicle_no','name'], ignore_index=True)

        #Merge df result with the df total to include total mileage
        dfresult = pd.merge(dfresult, dftotal, how='left', on='vehicle_no')

        #Finding percentage of cost distribution
        dfresult['percentage'] = dfresult['mileage'] / dfresult['total_mileage']

        print("Execution time (vehicle_mileage_percentage_in_all_area): {}".format(time.time()-start_time))
    except Exception as e: print(e)
    return dfresult

#start execution
start_time = time.time()

#Date range
start_dt = '2022-04-01 0:0:0'
end_dt = '2022-04-30 0:0:0'

#database connection
try:
    db_connection_url = "postgresql://postgres:test1234@localhost:5432/trackerfeed"
    con = create_engine(db_connection_url)
except Exception as e: print(e)

#calling three df function
dfarea = vehicle_traveled_in_all_area(start_dt,end_dt,con)

dftotal = total_mileage(start_dt,end_dt,con)

dfresult = vehicle_mileage_percentage_in_all_area(dfarea, dftotal)

#Output
print(dfresult)

#Save to percentage.csv
dfresult.to_csv('vehicle_total_mileage_percentage.csv', index=False)

print("Execution time (All) : {}".format(time.time()-start_time))

