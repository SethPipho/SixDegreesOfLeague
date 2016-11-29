  
#post process script for player history. 
#handles players with same Name
#filters out dates with question marks
#converts dates to single integer(months since 2000)
#outputs json
#converts all names to lower case

import os
import json
import sys
import unicodedata




fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"

inFile = open(os.path.join(fileDir, relPath, "playerInfoRaw.json"), "r", encoding="utf8")
outFile = open(os.path.join(fileDir, relPath, "playerInfo.json"), "w", encoding="utf8")


playerData = json.loads(inFile.read())


#Uniques fixes
playerData['Saiclone']["teams"][0]["end"] = "Sep 2015"
playerData['Rhuckz']["teams"][-1]["end"] = "Present" 
playerData['Malunoo']["teams"][2]["start"] = "Jan 2012" 
playerData['HoneyRain']["teams"][-1]["end"] = "Present" 
playerData['JothY']["teams"][0]["start"] = "Oct 2011" 
playerData['LaoPi']["teams"][5]["start"] = "Feb 2014" 



#remove teams where either start or end date is unknown
for player, data in playerData.items():
    for i in range(len(data['teams']) - 1,-1,-1):
        if "?" in data["teams"][i]["start"] or "?" in data["teams"][i]["end"]:
            data["teams"].pop(i)

#filter out caster position
for player, data in playerData.items():
    for i in range(len(data['teams']) - 1,-1,-1):
        if data["teams"][i]["position"].lower() == "caster":
            data["teams"].pop(i)

#filter out suspeneded
for player, data in playerData.items():
    for i in range(len(data['teams']) - 1,-1,-1):
        if data["teams"][i]["teamName"] == "":
            data["teams"].pop(i)



for player,data in playerData.items():

    print(player.encode("utf-8"))

    firstDate = 1000
    lastDate = 0

    playerData[player]["status"] = "inactive"

    for i,team in enumerate(data["teams"]):

        startDate = team["start"].strip().lower()
        endDate = team["end"].strip().lower()

        startMonth = startDate.split(" ")[0]
        startYear = startDate.split(" ")[-1]

        if endDate == "present":
            endMonth = 'dec'
            endYear = '2016'
            playerData[player]["status"] = "active"      
        else:
            endMonth = endDate.split(" ")[0]
            endYear = endDate.split(" ")[-1]
               
        
        months = {'jan':1, 'fed':2, 'feb':2, 'fev':2, 'mar':3, 'march':3, 'apr':4, 'april':4, 'abr':4, 'may':5, 'june':6, 'jun':6, 'jul':7,  'july':7,
        'aug':8, 'august':8, 'ago':8, 'sep':9, 'sept':9, 'spe':9, 'oct':10, 'october':10, 'nov':11, 'dec':12, 'dic':12, 'dez':12, 'late':12}

    
        #convert mdate into months since Jan 2000
        startNum = months[startMonth] + int(startYear[2:]) * 12
        endNum = months[endMonth] + int(endYear[2:]) * 12

        #track firstdate and last date for carreer start and finish
        if startNum < firstDate:
            firstDate = startNum
        if endNum > lastDate:
            lastDate = endNum

        #sometimes happens
        if startNum > endNum:
            endNum += 12

        playerData[player]["teams"][i]["start"] = startNum
        playerData[player]["teams"][i]["end"] = endNum

        playerData[player]["firstDate"] = firstDate
        playerData[player]["lastDate"] = lastDate





#set region they most recent played inm if change figure it out, set region to that of birthplace
teamFile = open(os.path.join(fileDir, relPath, "teamInfo.json"), "r", encoding="utf8")

teamInfo = json.loads(teamFile.read())

for player,data in playerData.items():

    try:
        team = data["teams"][-1]["teamName"]
        region = teamInfo[team]["region"]
        playerData[player]["currenTregion"] = region
    except:
         playerData[player]["currentRegion"] = "X"


#set region most played in


for player,data in playerData.items():

   
    regionsPlayed = {}
    print(player)

    for team in data["teams"]:
        if team == "":
            continue
        region = teamInfo[team["teamName"]]["region"]
        timePlayed = team["end"] - team['start']

        if region not in regionsPlayed:
            regionsPlayed[region] = 0
            
        regionsPlayed[region] += timePlayed
    
    times = []

    for region, time in regionsPlayed.items():
        times.append({"region":region, "time": time })
    
    times.sort(key= lambda t: t["time"])

    if len(times) > 0:
        playerData[player]["mostPlayedRegion"] = times[-1]["region"]
    else:
        print(playerData[player])
        playerData[player]["mostPlayedRegion"] = "X"


#convert all X regions into region of country

regions = {'New Zealand':"OCE",'Estonia':"EU",'Paraguay':"EU",'Slovenia':"EU", 'Thailand': 'SEA', "Austria":'EU','Bulgaria':"EU","Panama":"LA", 'South America': 'LA', 'Portugal': 'EU', 'Ukraine': 'RUSS', 'Denmark': 'EU', 'Japan': 'JAP', 'Norway': 'EU', 'Netherlands': 'EU', 'Philippines': 'SEA', 'Poland': 'EU', 'Czech Republic': 'EU', 'Hungary': 'EU', 'El Salvador': 'LA', 'United States': 'NA', 'Vietnam': 'SEA', 'Argentina': 'LA', 'Hong Kong': 'LMS', 'Uruguay': 'LA', 'Colombia': 'LA', 'Lithuania': 'EU', 'United Kingdom': 'EU', 'Chile': 'LA', 'Southeast Asia': 'SEA', 'Indonesia': 'SEA', 'Belgium': 'EU', 'Singapore': 'SEA', 'Spain': 'EU', 'Slovakia': 'EU', 'Venezuela': 'LA', 'North America': 'NA', 'Australia': 'OCE', 'Brazil': 'BR', 'Taiwan': 'LMS', 'Russia': 'RUSS', 'Canada': 'NA', 'Malaysia': 'SEA', 'Switzerland': 'EU', 'Germany': 'EU', 'San Diego, California': 'NA', 'Europe': 'EU', 'France': 'EU', 'unknown': 'X', 'Costa Rica': 'LA', 'Sweden': 'EU', 'Finland': 'EU', 'South Korea': 'KR', 'Peru': 'LA', 'Mexico': 'LA', 'Turkey': 'TR', 'China': 'CN', 'Italy': 'EU', 'Greece': 'EU'}
    

for player,data in playerData.items():
    if  playerData[player]["mostPlayedRegion"] == "X":
        playerData[player]["mostPlayedRegion"] = regions[playerData[player]["country"]]
  





        

outFile.write(json.dumps(playerData, indent=4, sort_keys=True))

outFile.close()
inFile.close()

   
