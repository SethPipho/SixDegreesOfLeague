
# coding: utf-8

import os
import requests
from bs4 import BeautifulSoup


fileDir = os.path.dirname(__file__)
relPath = "../datafiles/playerNames.txt"
outputPath = os.path.join(fileDir, relPath)

file = open(outputPath, "wb")

names = {}
urls = ["http://lol.esportswikis.com/wiki/Players_(NA)",
        "http://lol.esportswikis.com/wiki/Players_(Europe)",
        "http://lol.esportswikis.com/wiki/Players_(Asia)",
        "http://lol.esportswikis.com/wiki/Players_(All)",
        "http://lol.esportswikis.com/wiki/Players_(All)/Page_2"
        ]

for url in urls:
    print("fetching", url)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    rows = soup.find_all("table")[1].find_all("tr")

    for row in rows:
        try:
            cols = row.find_all("td")
            name = cols[0].get_text().strip()
            url = cols[0].find("a").get("href").strip()
            country = cols[3].get_text().strip()
            position = cols[4].get_text().strip()
            names[url] = {"name":name, "country":country,"position": position}
        except:
            pass

for key,val in names.items():
    try:
        #name,url, country,position
        file.write((val["name"] + "," + key + "," + val["country"] + "," + val["position"] + "\n").encode("utf-8"))
    except:
        print(key.encode("utf-8"), "contains crazy letters")
file.close()