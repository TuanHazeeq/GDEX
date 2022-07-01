import pandas as pd
from datetime import timedelta

df = pd.read_csv('triplog.csv')

#start_odometer is empty
print("start_odometer is empty:")
print(df['start_odometer'].isnull().sum())

#route_id is empty
print("route_id is empty:")
print(df['route_id'].isnull().sum())

#verifier_return_id is empty
print("verifier_return_id is empty:")
print(df['verifier_return_id'].isnull().sum())

#mileage is negative
mileage_df = df['end_odometer'].fillna(0)-df['start_odometer'].fillna(0)
print("mileage is negative:")
print((mileage_df<0).sum())

#Forgot to end trip for more than 1 day
fet_df = df.drop(df[df['end_odometer'].notnull()].index)
fet_df = fet_df.drop(fet_df[pd.to_datetime(fet_df['created_at'])>(pd.to_datetime('today').normalize()-timedelta(days=1))].index)
print("Forgot to end trip for more than 1 day:")
print(fet_df['id'].count())

#Wrong invalid flag
wif_df = df.drop(df[df['start_odometer'].isnull()].index)
wif_df = wif_df.drop(wif_df[wif_df['end_odometer'].isnull()].index)
wif_df = wif_df[wif_df['is_valid']==False]
wif_df = wif_df[(wif_df['end_odometer']-wif_df['start_odometer'])>=0]
print("Wrong invalid flag:")
print(wif_df['id'].count())

#Invalid destination
ivd = df['route_no'].str.contains('1|NA|N/A',regex=True)
ivd_df = numpy.where(ivd, df['route_no'])