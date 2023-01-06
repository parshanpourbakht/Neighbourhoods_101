import sys
import pandas as pd
import numpy as np



def main(rent_scoring_file, crime_scoring_file, amenity_scoring_file, output):
    rent = pd.read_csv(rent_scoring_file)
    crime = pd.read_csv(crime_scoring_file)
    amenity = pd.read_csv(amenity_scoring_file)


    rent_crime_merged = pd.merge(rent,crime,on='neighborhoods')

    scores = pd.merge(rent_crime_merged,amenity, on='neighborhoods')


    scores = scores[["neighborhoods", "rent_score", "crime_scores", "amenity_scores"]]



    scores['overall_scores'] = scores.sum(axis = 1)


    scores.to_csv(output)




if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])