
import os
import sys
import re
from multiprocessing.dummy import Pool
import requests
from bs4 import BeautifulSoup
import json



fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"

playerFile = open(os.path.join(fileDir, relPath, "playerNames.txt"), "r", encoding="utf-8")
outFile = open(os.path.join(fileDir, relPath, "playerInfoRaw.json"), "w", encoding="utf-8")
errorFile = open("errors/playerInfoErrors.txt", 'w')

players = []

for line in playerFile:
    s = line.strip().split(",")
    players.append({"name":s[0], "url":s[1], "country":s[2], "position":s[3], "teams":[] })


counter = 0


def getHistory(player):

    global counter 
    global errorFile
    counter += 1
    print("scraping", counter, "/", len(players) )

    url = "http://lol.esportswikis.com" + player["url"]

    try:
        r = requests.get(url)   
    
        data = r.text
        soup = BeautifulSoup(data, "lxml")

        header = soup.find_all('b', text = re.compile('Team History'))[0]
        tableTr = header.parent.parent
    
        table = tableTr.find_next('table')
        rows = table.find_all('tr')

        result = player

        for row in rows:
            cols = row.find_all('td')

            date = cols[0].get_text().strip()
            team = cols[1].find_all('span')[0].get_text().strip()

            position = cols[1].find_all("div")[0]["title"].strip()

            if (len(position) == 0):
                position = "Unknown"
            
    
            startDate = date.split("-")[0].strip()
            endDate = date.split("-")[1].strip()


            result["teams"].append({"teamName":team, "start":startDate, "end":endDate, "position":position})
            
    except Exception as e:
        errorFile.write(player["url"] + str(e) + "\n")
        return 
    
    return result

pool = Pool(32)


histories = pool.map(getHistory, players)



jsonList = {}

for item in histories:
    if item is not None:
            name = item['name']
            url = item["url"][6:].replace("_"," ")
            if url != name:
                jsonList[url] = item
                jsonList[url]["name"] = url
            else:
                jsonList[name] = item


outFile.write(json.dumps(jsonList, indent=4, sort_keys=True))

outFile.close()
playerFile.close()
errorFile.close()


