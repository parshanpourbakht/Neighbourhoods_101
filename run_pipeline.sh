#!/bin/sh

# ASCII escape codes for coloured output
RESET='\033[0m'
BOLDRED='\033[1;31m'
BOLDGREEN='\033[1;32m'
BOLDBLUE='\033[1;34m'  

PROMPT="$BOLDRED??$RESET"
RUN="${BOLDGREEN}RUN$RESET"
RUNNING="${BOLDGREEN}RUNNING$RESET"

# define commands and their descriptions

# CLEANING STEPS
DESC1="${BOLDGREEN}1-cleaning/filter-amenities.py${RESET}: \
Filter down to amenities in the city of vancouver"
CMD1="python3 1-cleaning/filter-amenities.py \
0-raw-data/amenities-lower-mainland.json.gz \
0-working-data/amenities-vancouver.json"

DESC2="${BOLDGREEN}1-cleaning/group-amenities.py${RESET}: \
Group amenity by neighbourhood"
CMD2="python3 1-cleaning/group-amenities.py \
0-raw-data/neighbourhood-boundaries.geojson \
0-working-data/amenities-vancouver.json \
0-working-data/grouped-amenities.geojson"

DESC3="${BOLDGREEN}1-cleaning/get_neighbourhoods.py${RESET}: \
Get neighbourhoods and their central coordinate"
CMD3="python3 1-cleaning/get_neighbourhoods.py \
0-raw-data/neighbourhood-boundaries.csv \
0-working-data/vancouver_neighbourhoods.csv"

DESC4="${BOLDGREEN}1-cleaning/get_rent_score.py${RESET}: \
Scrape average rent prices of neighbourhoods in vancouver"
CMD4="python3 1-cleaning/get_rent_score.py \
0-working-data/vancouver_rent_score.csv"

DESC5="${BOLDGREEN}1-cleaning/get_crime_score.py${RESET}: \
Get crime count and crime data of neighbourhoods in vancouver"
CMD5="python3 1-cleaning/get_crime_score.py \
0-raw-data/crimedata_csv_AllNeighbourhoods_2022.csv \
0-working-data/vancouver_crime_data.csv \
0-working-data/vancouver_crime_score.csv"

# ANALYSIS STEPS
DESC6="${BOLDGREEN}2-analysis/get_amenity_score.py${RESET}: \
Calculate scores for each neighbourhood using the 3 factor scoring metric"
CMD6="python3 2-analysis/get_amenity_score.py \
0-working-data/vancouver_neighbourhoods.csv \
0-working-data/amenities-vancouver.json \
0-working-data/amenities_by_neighbourhood.csv \
0-working-data/amenities_scores.csv"

DESC7="${BOLDGREEN}2-analysis/get_overall_score.py${RESET}: \
Combine 3 factor scores into overall neighbourhood scores"
CMD7="python3 2-analysis/get_overall_score.py \
0-working-data/vancouver_rent_score.csv \
0-working-data/vancouver_crime_score.csv \
0-working-data/amenities_scores.csv \
0-working-data/neighbourhood_scores.csv"

# show commands as numbered options to user
printf "$BOLDBLUE(1)$RESET CLEANING \n"
printf "\t$DESC1\n\t$DESC2\n\t$DESC3\n\t$DESC4\n\t$DESC5\n"
printf "$BOLDBLUE(2)$RESET ANALYSIS \n"
printf "\t$DESC6\n\t$DESC7\n"

mkdir -p 0-working-data

while : ; do
    printf "$PROMPT Select a step to run or q to quit: "; read -r ans
    case $ans in
        1)
            echo "STARTING CLEANING STEP"; 
            printf "$RUNNING $CMD1\n"
            $CMD1
            printf "$RUNNING $CMD2\n"
            $CMD2
            printf "$RUNNING $CMD3\n"
            $CMD3
            printf "$RUNNING $CMD4\n"
            $CMD4
            printf "$RUNNING $CMD5\n"
            $CMD5
            ;;
        2)
            echo "STARTING ANALYSIS STEP"; 
            printf "$RUNNING $CMD6\n"
            $CMD6
            printf "$RUNNING $CMD7\n"
            $CMD7
            ;;
        *)
            echo "Exiting..."; exit
            ;;
    esac
done
