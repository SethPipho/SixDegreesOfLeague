#automatically pulls of error links in browser for checking

import webbrowser

inFile = open("playerHistoryError.txt")
outFile = open("outstandingErrors.txt", "w")

for line in inFile:
    url = 'http://lol.esportswikis.com' + line.split("|")[0]
    webbrowser.open(url, new = 2)

    choice = input(url + " y/n")

    if choice == "n":
        outFile.write(line)

outFile.close()
inFile.close()

print("done")

