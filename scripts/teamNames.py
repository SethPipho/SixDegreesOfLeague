#gets all the team names from playersInfo.json

import json
import os

fileDir = os.path.dirname(__file__)
relPath = "../datafiles/"


playerFile = open(os.path.join(fileDir, relPath, "playerInfo.json"), "r", encoding="utf8")
nameFile = open(os.path.join(fileDir, relPath, "teamNames.txt"), "w", encoding="utf8")


players = json.loads(playerFile.read())

teamNames = []

for player, data in players.items():
    for team in data["teams"]:
        name = team["teamName"]

        if name not in teamNames:
            teamNames.append(name)

teamNames.sort()

for name in teamNames:
    nameFile.write(name + "\n")


playerFile.close()
nameFile.close()
