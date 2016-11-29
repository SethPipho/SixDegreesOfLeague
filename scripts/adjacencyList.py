
import json
import os

fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"


import os
import json
import sys
import unicodedata



fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"

inFile = open(os.path.join(fileDir, relPath, "playerInfo.json"), "r", encoding="utf8")


players = json.loads(inFile.read())


#determines if two dates overlap, returns time they started and ended working togehter
def overLap(a,b,c,d):
    if(a >= c and b <= d): 
        return [a,b]
    elif(a <= c and b >= d): 
        return [c,d]
    elif(a <= c and c < b): 
        return [c,b]
    elif(a >= c and a < d):
        return [a,d]
    return [0]

#returns all instance where player played with player b (info only on player a returned)
def playedTogether(playerA, playerB):

    teamsA = playerA["teams"]
    teamsB = playerB["teams"]

    sameTime = []

    for a in teamsA:
        for b in teamsB:
            if (a["teamName"] == b["teamName"]):
                overLapTime = overLap(a["start"], a["end"], b['start'], b['end'])
                if overLapTime[0] != 0 and overLapTime[1] - overLapTime[0] != 0:
                    data = {"teamName" : a["teamName"], "position":a["position"], "start":overLapTime[0], 'end': overLapTime[1]}
                    sameTime.append(data)
                    if (overLapTime[0] > overLapTime[1]):
                        print(playerA['name'], playerB['name'])
    return sameTime


adjacencyList = {}

print("creating complete List")
#created complete adjacencyList
for playerA in players.values():
    
    adjacencyList[playerA["name"]] = {}

    for playerB in players.values():
        if playerA["name"] == playerB["name"]:
            continue
       
        edges = playedTogether(playerA, playerB)
      
        if(len(edges) > 0):
            adjacencyList[playerA["name"]][playerB["name"]] = []
            for edge in edges:
                adjacencyList[playerA["name"]][playerB["name"]].append(edge)

listFile = open(os.path.join(fileDir, relPath, "adjacencyList.all.json"), "w", encoding="utf-8")
listFile.write(json.dumps(adjacencyList, indent=4))    
listFile.close()      

print("creating longest time spent together List")
#Filter adjacentcy by longest time spent together
adjacencyListFiltered = {}
count = 0

for player,edges in adjacencyList.items():
    adjacencyListFiltered[player] = {}
    for teamMate, teams in edges.items():
        if len(teams) > 0:
            teams.sort(key = lambda team: team["end"] - team["start"])
            adjacencyListFiltered[player][teamMate] = teams[-1]
           

listFile = open(os.path.join(fileDir, relPath, "adjacencyList.all.longestTimeTogether.json"), "w", encoding="utf-8")
listFile.write(json.dumps(adjacencyListFiltered, indent=4))
listFile.close()  



####Look at all this duplicated Code!

adjacencyList = {}

print("creating active List")
#created complete adjacencyList
for playerA in players.values():
  
    if (playerA["status"]) == "inactive":
        continue
    adjacencyList[playerA["name"]] = {}

    for playerB in players.values():
        if playerA["name"] == playerB["name"]:
            continue
        if playerB["status"] == "inactive":
            continue
       
        edges = playedTogether(playerA, playerB)
      
        if(len(edges) > 0):
            adjacencyList[playerA["name"]][playerB["name"]] = []
            for edge in edges:
                adjacencyList[playerA["name"]][playerB["name"]].append(edge)

listFile = open(os.path.join(fileDir, relPath, "adjacencyList.active.json"), "w", encoding="utf-8")
listFile.write(json.dumps(adjacencyList, indent=4))    
listFile.close()      

print("creating active longest time spent together List")
#Filter adjacentcy by longest time spent together
adjacencyListFiltered = {}
count = 0

for player,edges in adjacencyList.items():
    adjacencyListFiltered[player] = {}
    for teamMate, teams in edges.items():
        if len(teams) > 0:
            teams.sort(key = lambda team: team["end"] - team["start"])
            adjacencyListFiltered[player][teamMate] = teams[-1]
           

listFile = open(os.path.join(fileDir, relPath, "adjacencyList.active.longestTimeTogether.json"), "w", encoding="utf-8")
listFile.write(json.dumps(adjacencyListFiltered, indent=4))
listFile.close()  

