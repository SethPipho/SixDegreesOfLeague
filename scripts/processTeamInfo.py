


import json
import os


fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"


teamFile = open(os.path.join(fileDir, relPath, "teamInfo.raw.json"), "r", encoding="utf-8")
outFile = open(os.path.join(fileDir, relPath, "teamInfo.json"), "w", encoding="utf-8")


teamData = json.loads(teamFile.read())


regions = {'New Zealand':"OCE",'Estonia':"EU",'Paraguay':"EU",'Slovenia':"EU", 'Thailand': 'SEA', "Austria":'EU','Bulgaria':"EU","Panama":"LA", 'South America': 'LA', 'Portugal': 'EU', 'Ukraine': 'EU', 'Denmark': 'EU', 'Japan': 'JAP', 'Norway': 'EU', 'Netherlands': 'EU', 'Philippines': 'SEA', 'Poland': 'EU', 'Czech Republic': 'EU', 'Hungary': 'EU', 'El Salvador': 'LA', 'United States': 'NA', 'Vietnam': 'SEA', 'Argentina': 'LA', 'Hong Kong': 'LMS', 'Uruguay': 'LA', 'Colombia': 'LA', 'Lithuania': 'EU', 'United Kingdom': 'EU', 'Chile': 'LA', 'Southeast Asia': 'SEA', 'Indonesia': 'SEA', 'Belgium': 'EU', 'Singapore': 'SEA', 'Spain': 'EU', 'Slovakia': 'EU', 'Venezuela': 'LA', 'North America': 'NA', 'Australia': 'OCE', 'Brazil': 'BR', 'Taiwan': 'LMS', 'Russia': 'RUSS', 'Canada': 'NA', 'Malaysia': 'SEA', 'Switzerland': 'EU', 'Germany': 'EU', 'San Diego, California': 'NA', 'Europe': 'EU', 'France': 'EU', 'unknown': 'X', 'Costa Rica': 'LA', 'Sweden': 'EU', 'Finland': 'EU', 'South Korea': 'KR', 'Peru': 'LA', 'Mexico': 'LA', 'Turkey': 'TR', 'China': 'CN', 'Italy': 'EU', 'Greece': 'EU'}



for team,data in teamData.items():
    teamData[team]["region"] = regions[data["location"]]


teamData["Team Dignitas"]["region"] = "NA"
teamData["Team Liquid"]["region"] = "NA"
teamData["Team Liquid Academy"]["region"] = "NA"
teamData["Evil Geniuses"]["region"] = "EU"
teamData["Moscow Five"]["region"] = "EU"
teamData["LMQ"]["region"] = "NA"

outFile.write(json.dumps(teamData, indent=4, sort_keys=True))