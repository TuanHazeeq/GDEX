import glob, os
import fiona
import pandas as pd
import geopandas as gpd
from shapely import wkt

#Convert folder of kml to one csv
def kml_to_csv(folder_loc):
    #Enable KML as driver for geopandas
    gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    alldf = pd.DataFrame()

    os.chdir(folder_loc)
    #Read all files with .kml file extension
    for kmlfiles in glob.glob("*.kml"):

        #For branch_no
        kmlfile = kmlfiles.replace('.kml','')

        #For every layer of .kml file EX.:GDEX BRANCH, MOTOR ROUTE COVERAGE, VAN ROUTE COVERAGE
        for layer in range(len(fiona.listlayers(kmlfiles))):
            print(kmlfile)
            #First layer of .kml file
            if(layer==0):
                df = gpd.read_file(kmlfiles,driver='KML')
            #Other layers of .kml file
            else:
                df = gpd.read_file(kmlfiles, driver='KML', layer = fiona.listlayers(kmlfiles)[layer])

            #Change 3d polygon and point to 2d polygon and point
            df['geometry'] = df['geometry'].astype('string')
            df['geometry'] = df['geometry'].str.replace(' Z ','')
            df['geometry'] = df['geometry'].str.replace(' 0,',',')
            df['geometry'] = df['geometry'].str.replace(' 0\)',')',regex=True)
            df['geometry'] = df['geometry'].apply(wkt.loads)
            print(df['geometry'])
            df = df.set_geometry('geometry')

            #Uses layer's name as route type
            df['route_type'] = fiona.listlayers(kmlfiles)[layer]
            # Use file name as branch no
            df['branch_no'] = kmlfile
            alldf = pd.concat([alldf,df], ignore_index=True)

    alldf.to_csv('route2.csv')

path = 'convert'
kml_to_csv(path)