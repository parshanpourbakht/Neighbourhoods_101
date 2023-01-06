import sys
import pandas as pd
import geopandas as gpd


def main(boundaries_file, amenities_file, output_file):
    boundaries = gpd.read_file(boundaries_file)
    amenities = pd.read_json(amenities_file, lines=True)

    boundaries = boundaries.drop("mapid", axis=1) # remove unneeded column
    # create a GeoDataFrame and include a geometry column to store
    # the coordinate location of each amenity
    amenities = gpd.GeoDataFrame(amenities, 
            geometry=gpd.points_from_xy(amenities.lon, amenities.lat))

    # use a point in polygon query to group amenities into neighbourhoods
    # if it is located inside the neighbourhood
    # reference: https://medium.com/analytics-vidhya/point-in-polygon-analysis-using-python-geopandas-27ea67888bff
    amenities["neighbourhood"] = None
    # find amenities for each neighbourhood in the boundaries dataset
    for i in range(len(boundaries)):
        # get a column mask for the amenities within the neighbourhood
        is_in_boundary = amenities.within(boundaries.loc[i, "geometry"])
        # set the neighbourhood of amenities that are within the neighbourhood
        amenities.loc[is_in_boundary, "neighbourhood"] = \
                boundaries.loc[i, 'name']

    # drop the amenities that are not within a neighbourhood
    grouped_amenities = amenities.dropna().reset_index(drop=True)

    grouped_amenities.to_file(output_file, driver="GeoJSON")

    # convert to pandas dataframe to write data to regular json
    amenities = pd.DataFrame(grouped_amenities)\
            .drop(["geometry"], axis=1)

    # filter amenities down to only the 22 neighbourhood amenities
    amenities.to_json(amenities_file, lines=True, orient="records")



if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
