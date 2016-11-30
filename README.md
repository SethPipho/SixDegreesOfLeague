# SixDegreesOfLeague
Six Degrees of Separation with professional League of Legends Players


Six Degrees of League is a project that analyzes how professional League of Legends 
players are connected.

Player and Team data was scraped from [lol.esportswikis](http://lol.esportswikis.com/) using 
BeautifulSoup scraping library from python. Another set of scripts scrubs the data to remove or 
correct bad data. For example, if player A is listed on being team be from ??? 2013 to Feb 2014,
the data is removed due to uncertainty. Scrubbing also involves things like handling dates spelled wrong,
players with same name, or misc. errors that need to be handled individually. The scrubbing process
was by far the most time-consuming (and annoying) process of this project.

Next step is to build an adjacency list which, for every player, lists who they have been on the
same team with. The python script produces two versions of this list, one with every instance where
two players played together, and other that lists only the time they spent the longest together.


This adjacency list in converted to a .gdf file and imported into [Gephi](https://gephi.org/), a network
visualization tool. 

The color of each node denotes what region they played the longest in. The size of a node represent the length
of the player's career. The connections between players are weighted by how long the spent together, eg teams
of players who have played together for a long time tend to cluster together.

![Alt text](http://i.imgur.com/ezfDIcw.jpg)




