import sys
import pandas as pd


def main(lower_mainland_file, output_file):
    lower_mainland = pd.read_json(lower_mainland_file, lines=True, compression="gzip")

    # filter down to only amenity name and coordinate
    lower_mainland = lower_mainland[['lat', 'lon', 'amenity']]
    # filter down to the city of vancouver
    north_lat = 49.3003
    south_lat = 49.1947
    west_lon = -123.2683
    east_lon = -123.0173
    vancouver = lower_mainland[
            lower_mainland["lat"].between(south_lat, north_lat) &
            lower_mainland["lon"].between(west_lon, east_lon)
        ]

    # visualization of filtering, before and after
    # import plotly.express as px
    # px.set_mapbox_access_token(open(".mapbox_token").read())
    # fig = px.scatter_mapbox(data_frame=lower_mainland, lat='lat', lon='lon', zoom=10)
    # fig.show() # before
    # fig = px.scatter_mapbox(data_frame=vancouver, lat='lat', lon='lon', zoom=10)
    # fig.show() # after

     # major amenitiy list to filter with 
    major_amenities_list = ['school', 'restaurant','pharmacy', 'bank', 
    'community_centre', 'fuel', 'dentist', 'doctors', 'hospital']
    # filter for major amenities
    
    vancouver =  vancouver[vancouver['amenity'].isin(major_amenities_list)]\
            .reset_index(drop=True)

    vancouver.to_json(output_file, lines=True, orient="records")


if __name__=='__main__':
    main(sys.argv[1], sys.argv[2])
