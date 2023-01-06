import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import sys

def main(output):
    #Make page request for HTML page data
    page = requests.get("https://www.vancouverisawesome.com/local-news/here-is-how-much-it-costs-to-rent-in-each-vancouver-neighbourhood-right-now-5164211")
    soup = BeautifulSoup(page.content, 'html.parser')


    rentNeighborHtmlData = []
    neighborhoods = []
    rents = []

    #Retrived html container container the list Vancouver neighbourhoods and rent prices
    for row in soup.find_all("div", id="details-body")[0].findAll("td"):
        rentNeighborHtmlData.append(str(row))

    #Iterate through every HTML table data value and retrieve neighbourhood name and rent using Regex
    for n in rentNeighborHtmlData:

        #regex for finding neighborhood namea and rent prices
        neighborhood_re = re.search(r'\">(.*)</a></td>', n)
        rent_re = re.search(r'>\$(.*)</td>', n)


        if neighborhood_re:
            neighborhoods.append(''.join(neighborhood_re.groups()))

        if rent_re:
            rent_value = ''.join(rent_re.groups())
            rents.append(int(re.sub(",","",rent_value)))

    neighborhood_rent_df = pd.DataFrame({'neighborhoods':neighborhoods, 'rent':rents})


    # extra rows to remove
    neighborhoods_to_disclude = ["University Endowment Lands", "Quilchena"]
    neighborhood_rent_df = neighborhood_rent_df[~neighborhood_rent_df['neighborhoods'].isin(neighborhoods_to_disclude)]

    #renaming of neighborhoods to be consistent with data pipeline
    #rename because these neighborhoods may have differnt spelling or given a different name but are the same neighborhood
    neighborhood_rent_df = neighborhood_rent_df.replace({'neighborhoods':{"Arbutus":"Arbutus Ridge", "Mt. Pleasant":"Mount Pleasant",
        "Riley Park - Little Mountain":"Riley Park", "South Granville":"Shaughnessy", "Cambie":"South Cambie", "Dunbar":"Dunbar-Southlands",
        "Downtown Vancouver":"Downtown"}})


    #creates scores from 0-10, score are based off rent prices
    #low scores means high rent 
    #high scores mean low rent 
    neighborhood_rent_df['rent_score'] = 10 - ((neighborhood_rent_df["rent"]-min( neighborhood_rent_df["rent"]))/ \
        (max( neighborhood_rent_df["rent"])-min( neighborhood_rent_df["rent"])) * 10)


    neighborhood_rent_df.to_csv(output, index=False)



if __name__=='__main__':
    main(sys.argv[1])