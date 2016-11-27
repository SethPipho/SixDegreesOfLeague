
import os
import sys
import re
from multiprocessing.dummy import Pool
import requests
from bs4 import BeautifulSoup



fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"

playerFile = open(os.path.join(fileDir, relPath, "playerNames.txt"), "r", encoding="utf-8")
outFile = open(os.path.join(fileDir, relPath, "playerInfoRaw.txt"), "wb")


players = []

for line in playerFile:
    s = line.strip().split(",")
    players.append({"name":s[0], "url":s[1], "country":s[2], "position":s[3] })


counter = 0
failures = []


def getHistory(player):

    global counter 
    global failures
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

        result = [player["name"], player['url'] , player["country"], player["position"]]

        for row in rows:
            cols = row.find_all('td')

            date = cols[0].get_text().strip()
            team = cols[1].find_all('span')[0].get_text().strip()

            position = cols[1].find_all("div")[0]["title"].strip()

            if (len(position) == 0):
                position = "Unknown"
            
    
            startDate = date.split("-")[0].strip()
            endDate = date.split("-")[1].strip()


            result.append(team)
            result.append(position)
            result.append(startDate)
            result.append(endDate)
            
    
    except:
        failures.append([player["url"], sys.exc_info()[0]])
        return 
    
    if len(result) == 1:
        return 

    return "|".join(result)

pool = Pool(32)


histories = pool.map(getHistory, players)



errorFile = open("errors/playerInfoErrors.txt", 'w')

for item in failures:
   errorFile.write(item[0])
   errorFile.write("|")
   errorFile.write(str(item[1]))
   errorFile.write("\n")
   

for item in histories:
    if item is not None:
        outFile.write(item.encode('utf-8') + '\n'.encode('utf-8'))

outFile.close()
playerFile.close()
errorFile.close()


