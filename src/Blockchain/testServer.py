from nodo import *

hosts_list = [["172.16.3.98", "172.16.3.130"]]

myHost = "172.16.3.98"
myLeader = "172.16.3.98"
blockchainPath = "./TestBC"
toleranceValue = 0.5
voteUmbral = 2

yo = NodoSufAndComis(myHost, 9991, hosts_list, 0, myLeader, toleranceValue, voteUmbral, blockchainPath)


