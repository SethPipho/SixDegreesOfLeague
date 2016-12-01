import json
import os
import time

fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"

adjacencyFile = open(os.path.join(fileDir, relPath, "adjacencyList.all.longestTimeTogether.json"), "r", encoding="utf-8")
pathFile = open(os.path.join(fileDir, relPath, "allPaths.txt"), "w", encoding="utf-8")

players = json.loads(adjacencyFile.read())

def BFS(root, target, graph):

    visted = {}
    parent = {}
    path = []

    count = 0

    for key in graph.keys():
        visted[key] = False
        parent[key] = ""

    visted[root] = True

    Queue = []
    Queue.append(root) 

    while len(Queue) != 0:
        current = Queue.pop()
        
        for adjacent in graph[current].keys():
            if visted[adjacent] == False:
                visted[adjacent] = True
                parent[adjacent] = current
                Queue.insert(0,adjacent)
            
            if adjacent == target:
               path.append([target, graph[target][parent[target]]["teamName"]])
               while current != root:
                   path.append([current, graph[parent[current]][current]["teamName"]])
                   current = parent[current]
               path.append(root)
               return path
    path.append("None")
    return path

while True:
    player1 = input("player 1:")
    player2 = input("player2:")
    print(BFS(player1, player2, players))


#convert dict to list to maintain alphabetical order
playerList = [name.lower() for name in players.keys()]
playerList.sort()

paths = []
count = 0
startTime = time.time()

for i in range(len(playerList) - 1):
    for k in range(i + 1, len(playerList)):
        path = BFS(playerList[i], playerList[k], players)
        paths.append(playerList[i] + "|" + playerList[k] + "|" + "|".join(path))
        
        count += 1
        #write path to file every 10,000 so things doesn not exploade at end
        if count % 10000 == 0:
            print(count, time.time() - startTime)
            pathFile.write("\n".join(paths))
            paths = [] 

pathFile.write("\n".join(paths))
            
            





            
        

