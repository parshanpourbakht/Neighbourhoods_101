import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from geopy.geocoders import Nominatim
import sys


def getLatLon(row):
    address = str(row[0]) + ", Vancouver"
    nom = Nominatim(user_agent="application")
    n = nom.geocode(address)
    return pd.Series([n.latitude, n.longitude])


output_file = sys.argv[1]

#Make page request for HTML page data
page = requests.get("https://en.wikipedia.org/wiki/List_of_neighbourhoods_in_Vancouver#Official_neighbourhoods")
soup = BeautifulSoup(page.content, 'html.parser')

neighborhoodHtmlData = []
neighborhoods = []

#Retrived html container container the list of Official Vancouver neighbourhoods
for row in soup.find_all("div", class_="navbox")[0].findAll("li"):
  neighborhoodHtmlData.append(str(row))

#Iterate through every list item and retrieve neighbourhood name using Regex
for n in neighborhoodHtmlData:
    if len(n) == 0:
        neighborhoodHtmlData.remove(n)
    else:
        m = re.search(r'\">(.*)</a></b></li>', n)
        if m:
            neighborhood = re.sub(",", "", (''.join(m.groups())))

            neighborhoods.append(neighborhood)

df = pd.DataFrame(neighborhoods)
df.columns = ['Neighborhoods']

df[['lat','lon']] = df.apply(getLatLon, axis=1)
print(df)

df.to_csv(output_file, index=False)
