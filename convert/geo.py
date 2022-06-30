from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import time

#database connection
try:
    db_connection_url = "postgresql://postgres:test1234@localhost:5432/trackerfeed"
    con = create_engine(db_connection_url)
except Exception as e: print(e)

sql="""SELECT a.*, b.polygon FROM gdex.org_branch a
LEFT JOIN branchpolygon b ON a.origin_code = b.name
ORDER BY a.id"""
df = pd.read_sql(sql, con)

#Output
df.to_csv('org_branch.csv', index=False)
df = pd.read_csv('org_branch.csv')
print(df)
