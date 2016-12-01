#converys adjancy list into sif file for cytoscape


import os
import json
import sys


fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"

adjFile = open(os.path.join(fileDir, relPath, "adjacencyList.all.longestTimeTogether.json"), "r", encoding="utf8")
gdfFile = open(os.path.join(fileDir, relPath, "network.gdf"), "w", encoding="utf8")

playerFile = open(os.path.join(fileDir, relPath, "playerInfo.json"), "r", encoding="utf8")



adjList = json.loads(adjFile.read())
playerData = json.loads(playerFile.read())



nodes = []
edges = []

for player,teamMates in adjList.items():
    if len(playerData[player]['teams']) < 1 or len(teamMates.keys()) < 1:
        continue
    nodes.append([player, str(playerData[player]["lastDate"] -  playerData[player]["firstDate"]), playerData[player]["mostPlayedRegion"]])
    for teamMate,team in teamMates.items():
        edges.append([player,teamMate, str(team["end"] - team["start"])])
    
gdfFile.write("nodedef>name VARCHAR, size DOUBLE, region VARCHAR\n")

for node in nodes:
    gdfFile.write(",".join(node) + "\n")

gdfFile.write("edgedef>node1 VARCHAR,node2 VARCHAR, weight DOUBLE\n")

for edge in edges:
    gdfFile.write(",".join(edge) + "\n")