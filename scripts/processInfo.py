  
#post process script for player history. 
#handles players with same Name
#filters out dates with question marks
#converts dates to single integer(months since 2000)
#outputs json
#converts all names to lower case

import os
import json
import pprint
import sys
import unicodedata


pp = pprint.PrettyPrinter(indent=4)

fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"

inFile = open(os.path.join(fileDir, relPath, "playerInfoRaw.fixed.txt"), "r", encoding="utf8")
jsonFile = open(os.path.join(fileDir, relPath, "playerInfo.json"), "w", encoding="utf8")

players = []



lineNum = 0
#convert date to integers
for line in inFile:
    

    lineNum += 1  
    print(lineNum)

    parts = line.split("|")

    name = parts[0]
   
    url = parts[1]
    country = parts[2]
    role = parts[3]

    player = {"name":name, "url":url, "country":country, "role":role,"status":"inactive", "teams":[]}

    for i in range(4, len(parts), 4):

        teamName = parts[i] 
        position = parts[i+1]
        startDate = parts[i+2].strip().lower()
        endDate = parts[i+3].strip().lower()

        if "?" in startDate or "?" in endDate:
            continue
        
        if position == "Unknown":
            position = role
        elif position == "Caster":
            continue


        startMonth = startDate.split(" ")[0]
        startYear = startDate.split(" ")[-1]

        if endDate == "present":
            endMonth = 'nov'
            endYear = '2016'
            player["status"] = "active"
           
        else:
            endMonth = endDate.split(" ")[0]
            endYear = endDate.split(" ")[-1]
        
        months = {'jan':1, 'fed':2, 'feb':2, 'fev':2, 'mar':3, 'march':3, 'apr':4, 'april':4, 'abr':4, 'may':5, 'june':6, 'jun':6, 'jul':7,  'july':7,
         'aug':8, 'august':8, 'ago':8, 'sep':9, 'sept':9, 'spe':9, 'oct':10, 'october':10, 'nov':11, 'dec':12, 'dic':12, 'dez':12, 'late':12}

       
        #convert mdate into months since Jan 2000
        startNum = months[startMonth] + int(startYear[2:]) * 12
        endNum = months[endMonth] + int(endYear[2:]) * 12

       
        player["teams"].append({"teamName": teamName, "start":startNum, "end":endNum, "position":position})
        

    
    players.append(player)

#rename duplicates

players = sorted(players, key= lambda p: p["name"])

duplicates = []

for i in range(len(players) - 2, -1, -1):

    if players[i]["name"] == players[i + 1]["name"]:
        if  players[i]["name"] != players[i + 2]["name"]:
            duplicates.append(players.pop(i+1))
            duplicates.append(players.pop(i))
        else:
            duplicates.append(players.pop(i))

#rename with name given in url eg (/wiki/sneaker_(Stan_Smith))
for i,item in enumerate(duplicates):
    url = item['url']
    index = url.find("_")

    if index != -1:
        name = url[index + 1:].replace("_", " ")
        duplicates[i]['name'] += name
        
    players.append(duplicates[i])


#get rid of special characters
for i in range(len(players)):
    players[i]["name"] = unicodedata.normalize('NFKD', players[i]["name"].lower())
   
   
players = sorted(players, key= lambda p: p["name"])

jsonFile.write(json.dumps(players, indent=4, sort_keys=True))

jsonFile.close()
inFile.close()

   
