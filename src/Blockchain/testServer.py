from nodo import *

hosts_list = [["192.168.1.4", "192.168.1.6"]]

myHost = "192.168.1.4"
myLeader = "192.168.1.4"
toleranceValue = 0.5
voteUmbral = 2

yo = NodoSufAndComis(myHost, 9991, hosts_list, 0, myLeader, toleranceValue, voteUmbral)


