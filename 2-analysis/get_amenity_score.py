import sys
import pandas as pd
# import requests
from sklearn.metrics.pairwise import haversine_distances
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler




def calculatePriority(amenities_data):
    #group amenitiy df by alike amentities and get thier counts
    amenities_counts = amenities_data.groupby("amenity").size().reset_index()
    amenities_counts.columns = ['amenity', 'counts']

    #get total of all amenities in df
    total_amentiy_count = amenities_counts['counts'].sum()

    #calculate proportion of each amenity by count/total
    amenities_counts['overall_proportion'] = amenities_counts['counts'] / total_amentiy_count

    #sort values in decreasing order and use indexes to rank amenities in priority
    amenities_counts =  amenities_counts.sort_values('overall_proportion', ascending=False).reset_index(drop=True).reset_index()
    amenities_counts.columns = ['priority', 'amenity', 'counts', 'overall_proportion']
    amenities_counts['priority'] += 1

    return amenities_counts


def calculateDistance(neighborhoods, major_amenities_df):
    # calculates distance (km) between every amenity and every neighborhood
    # source: https://stackoverflow.com/questions/71658779/how-how-to-calculate-haversine-cross-distance-between-to-pandas-dataframe 
    distances = pd.DataFrame(
        haversine_distances(
            np.radians(neighborhoods[['lat','lon']]),
            np.radians(major_amenities_df[['lat','lon']])
        ) * 6371,# mean radius of earth
        index=neighborhoods.name, columns=major_amenities_df.amenity)

    # get min distance for each amenity
    min_distance = distances.min().reset_index()
    min_distance.columns = ['amenity', "nearest_neighborhood_distance"]
    min_distance = min_distance.drop('amenity', axis=1)

    # get nearest neighborhood 
    min_neighorhood = distances.idxmin().reset_index()
    min_neighorhood.columns = ['amenity', "nearest_neighborhood"]
    min_neighorhood = min_neighorhood.drop('amenity', axis=1)

    # join data 
    amenities_data = pd.merge(major_amenities_df, min_neighorhood,
                              left_index=True, right_index=True)
    amenities_data = pd.merge(amenities_data, min_distance,
                              left_index=True, right_index=True)

    return amenities_data


def calculateNeighborhoodAmenityScores(amenities_data, amenities_priority):

    #do a left join on wiht the amenities df and the amenity priority df to get individual priorities 
    #each amenity
    amenities_data = amenities_data.merge(amenities_priority, on='amenity', how='left')

    #group by nearest_neighborhood and calculate the mean of the priorities for each of the amenities in 
    #the neighbourhood
    avg_neighbourhood_priorities =  amenities_data.groupby("nearest_neighborhood")['priority'].mean().reset_index()


    #normalizing data to get a amenity score from 0-10 
    avg_neighbourhood_priorities["amenity_scores"] = (avg_neighbourhood_priorities["priority"]-min(avg_neighbourhood_priorities["priority"]))/ \
        (max(avg_neighbourhood_priorities["priority"])-min(avg_neighbourhood_priorities["priority"])) * 10

    return avg_neighbourhood_priorities


def main(neighborhood_file, amenities_file, output_file1, output_file2):
    neighborhoods = pd.read_csv(neighborhood_file)
    major_amenities_df = pd.read_json(amenities_file, lines=True)

    # adds distances and nearest neighbourhood columns in df for each ameniy 
    amenities_data = calculateDistance(neighborhoods, major_amenities_df)

    # implement KMean clustering based off of lat and lon values
    kmeans = KMeans(22)
    x = amenities_data.iloc[:,0:2]
    kmeans.fit(x)
    identified_clusters = kmeans.fit_predict(x)

    # get controid/cluster centers 


    # merge cluster values for each row back to original dataframe

    clusters = pd.DataFrame(identified_clusters)
    clusters.columns = ['cluster']
    amenities_data = pd.merge(amenities_data, clusters, left_index=True, 
                              right_index=True)

    amenities_priority = calculatePriority(amenities_data)

    amenities_with_scores = calculateNeighborhoodAmenityScores(amenities_data, amenities_priority)

    amenities_with_scores.columns = ["neighborhoods", "priority", "amenity_scores"]

    centroids_df = pd.DataFrame(kmeans.cluster_centers_)

    centroids_df.columns = ["centroid_lat", "centroid_lon"]

    amenities_with_scores = amenities_with_scores.join(centroids_df)


    amenities_with_scores.to_csv(output_file2, index=False)
    amenities_data.to_csv(output_file1, index=False)


if __name__=='__main__':
    neighborhood_file = sys.argv[1]
    amenities_file = sys.argv[2]
    output_file1 = sys.argv[3]
    output_file2 = sys.argv[4]

    main(neighborhood_file, amenities_file, output_file1, output_file2)
