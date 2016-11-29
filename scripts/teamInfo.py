#scrapes team info from wiki



import os
import sys
import re
from multiprocessing.dummy import Pool
import requests
from bs4 import BeautifulSoup
import json


fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"


nameFile = open(os.path.join(fileDir, relPath, "teamNames.txt"), "r", encoding="utf-8")
outFile = open(os.path.join(fileDir, relPath, "teamInfo.raw.json"), "w", encoding="utf-8")

errorFile = open("errors/teamInfoErrors.txt", 'w', encoding="utf-8")


names = []
count = 0

for line in nameFile:
    names.append(line.strip())



def getTeamInfo(name):

    global errorFile
    global count 

    count += 1
    print(count)

    #print(name)

    url = "http://lol.esportswikis.com/wiki/" + name.replace(" ", "_")

    try:
        r = requests.get(url)   
        data = r.text
        soup = BeautifulSoup(data, "lxml")

        locTag = soup.findAll('th', text = re.compile(' Location:'))[0]
        loc = locTag.parent.findAll('td')[0].get_text().strip()

        #print(loc)

    except Exception as e:
        errorFile.write(name + "," + str(e) + "\n")
        return("unknown")
    
    return(loc)



pool = Pool(32)

locations = pool.map(getTeamInfo, names)


jsonList = {}

for i in range(len(names)):
    jsonList[names[i]] = {"location":locations[i]}



outFile.write(json.dumps(jsonList, indent=4, sort_keys=True))
