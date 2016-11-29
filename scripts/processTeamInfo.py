


import json
import os


fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"


teamFile = open(os.path.join(fileDir, relPath, "teamInfo.raw.json"), "r", encoding="utf-8")
outFile = open(os.path.join(fileDir, relPath, "teamInfo.json"), "w", encoding="utf-8")


teamData = json.loads(teamFile.read())

#unique fixes
teamData["Team Dignitas"]["location"] = "United States"
teamData["Team Liquid"]["location"] = "United States"


#used to generate reagion list
"""
locations = []

for team,data in teamData.items():
    
    if data["location"] not in locations:
        locations.append(data["location"])

for location in locations:
    print(location.encode("utf-8"))
    region = ""
    while region not in ["NA", "EU","KR", "CN", "SEA", "BR", "LA", "JAP", "TR", "RUSS", "OCE" ,"X","LMS"]:
        region = input()
    regions[location] = region

print(regions)
"""




regions = {'New Zealand':"OCE",'Estonia':"EU",'Paraguay':"EU",'Slovenia':"EU", 'Thailand': 'SEA', "Austria":'EU','Bulgaria':"EU","Panama":"LA", 'South America': 'LA', 'Portugal': 'EU', 'Ukraine': 'RUSS', 'Denmark': 'EU', 'Japan': 'JAP', 'Norway': 'EU', 'Netherlands': 'EU', 'Philippines': 'SEA', 'Poland': 'EU', 'Czech Republic': 'EU', 'Hungary': 'EU', 'El Salvador': 'LA', 'United States': 'NA', 'Vietnam': 'SEA', 'Argentina': 'LA', 'Hong Kong': 'LMS', 'Uruguay': 'LA', 'Colombia': 'LA', 'Lithuania': 'EU', 'United Kingdom': 'EU', 'Chile': 'LA', 'Southeast Asia': 'SEA', 'Indonesia': 'SEA', 'Belgium': 'EU', 'Singapore': 'SEA', 'Spain': 'EU', 'Slovakia': 'EU', 'Venezuela': 'LA', 'North America': 'NA', 'Australia': 'OCE', 'Brazil': 'BR', 'Taiwan': 'LMS', 'Russia': 'RUSS', 'Canada': 'NA', 'Malaysia': 'SEA', 'Switzerland': 'EU', 'Germany': 'EU', 'San Diego, California': 'NA', 'Europe': 'EU', 'France': 'EU', 'unknown': 'X', 'Costa Rica': 'LA', 'Sweden': 'EU', 'Finland': 'EU', 'South Korea': 'KR', 'Peru': 'LA', 'Mexico': 'LA', 'Turkey': 'TR', 'China': 'CN', 'Italy': 'EU', 'Greece': 'EU'}



for team,data in teamData.items():
    teamData[team]["region"] = regions[data["location"]]



outFile.write(json.dumps(teamData, indent=4, sort_keys=True))