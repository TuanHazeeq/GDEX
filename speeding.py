from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import time

#List vehicles speeding above 70km/h
def speeding(start_dt, end_dt, con):
    df = pd.DataFrame()
    try:
        sql = """SELECT vehicle_no, speed FROM gdex.vtracker_trackeralert
        WHERE time_stamp >= \'{}\' AND time_stamp < \'{}\'
        AND speed >=70
        ORDER BY vehicle_no, time_stamp"""
        sql = sql.format(start_dt, end_dt)
        df = pd.read_sql(sql, con)

        df80 = df[(df['speed']>=80) & (df['speed']<90)]
        df80 = df80.groupby('vehicle_no')['speed'].agg(['count']).reset_index()
        df80.rename(columns= {'count':'80-90'}, inplace = True)

        df90 = df[(df['speed']>=90) & (df['speed']<100)]
        df90 = df90.groupby('vehicle_no')['speed'].agg(['count']).reset_index()
        df90.rename(columns= {'count':'90-100'}, inplace = True)

        df100 = df[(df['speed']>=100) & (df['speed']<110)]
        df100 = df100.groupby('vehicle_no')['speed'].agg(['count']).reset_index()
        df100.rename(columns= {'count':'100-110'}, inplace = True)

        df110 = df[df['speed']>=110]
        df110 = df110.groupby('vehicle_no')['speed'].agg(['count']).reset_index()
        df110.rename(columns= {'count':'>=110'}, inplace = True)

        df = pd.merge(df80,df90,  on='vehicle_no', how='outer')
        df = pd.merge(df,df100,  on='vehicle_no', how='outer')
        df = pd.merge(df,df110,  on='vehicle_no', how='outer')
        df = df.fillna(0)
        df['total_speeding_count'] = df['80-90'] + df['90-100'] + df['100-110'] + df['>=110']
        print(df)

    except Exception as e: print(e)
    return df

#database connection
try:
    db_connection_url = "postgresql://postgres:test1234@localhost:5432/trackerfeed"
    con = create_engine(db_connection_url)
except Exception as e: print(e)

start_dt = '2022-04-04 0:0:0'
end_dt = '2022-04-05 0:0:0'

df = speeding(start_dt, end_dt, con)
df.to_csv('speeding.csv', index=False)