import sys
import pandas as pd
import numpy as np
import utm


def utm_to_latlon(x, y):
    #used to convert from utm zone 10 to lat lon 
    #https://stackoverflow.com/questions/6778288/lat-lon-to-utm-to-lat-lon-is-extremely-flawed-how-come 
    lat, lon = utm.to_latlon(488843.7729, 5.454999e+06, 10, 'U')
    return lat, lon


def main(vpd_crime_file, output1, output2):
    crime_data = pd.read_csv(vpd_crime_file)
    crime_data = crime_data[['TYPE', 'NEIGHBOURHOOD', 'X', 'Y']]
    crime_data.columns = ['crime_type', 'neighborhoods', 'x', 'y']

    utm_converter = np.vectorize(utm_to_latlon)
    
    tup = utm_converter(crime_data['x'], crime_data['y'])

    crime_data['lat'] = tup[0]
    crime_data['lon'] = tup[1]

    neighborhoods_to_disclude = ["Stanley Park", "Musqueam"]
    crime_data = crime_data[~crime_data['neighborhoods'].isin(neighborhoods_to_disclude)]

    crime_data = crime_data.replace({'Central Business District': 'Downtown'})


    crime_counts = crime_data.groupby("neighborhoods").size().reset_index()
    crime_counts.columns = ['neighborhoods', 'counts']


    #normalizing crime scores (from 0-10) based off of crime counts
    #the lower the score, the safer the neighborhood
    #the higher the score, the more unsafe the neighborhood
    crime_counts["crime_scores"] = 10 - ((crime_counts["counts"]-min(crime_counts["counts"]))/ \
        (max(crime_counts["counts"])-min(crime_counts["counts"])) * 10)

    crime_scores = crime_counts

    

    crime_data.to_csv(output1, index=False)
    crime_scores.to_csv(output2, index=False)


if __name__=='__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])