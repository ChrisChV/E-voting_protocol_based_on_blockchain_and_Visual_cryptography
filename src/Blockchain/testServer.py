from nodo import *
import sys;


SERVER_HOSTS_FILE_PATH = "../Conf/serverHosts"

myHost = "192.168.1.13"


def getHostList(fileName):
    myIdGroup = 0
    file = open(fileName, 'r')
    ips = []
    groupsIDs = []
    for line in file:
        tokens = line.split(" ")
        print(tokens)
        ips.append(tokens[1])
	print(tokens[1])
	if(tokens[1] == myHost):
	    print("AAA")
	    myIdGroup = int(tokens[3].rstrip('\n'))
        groupsIDs.append(int(tokens[3].strip('\n')))
    hosts_list = []
    numOfGroups = max(groupsIDs) + 1
    for i in range(0, numOfGroups):
        hosts_list.append([])
    for i in range(0, len(ips)):
        hosts_list[groupsIDs[i]].append(ips[i])
    file.close()
    return hosts_list, myIdGroup

#hosts_list = [["192.168.1.10", "192.168.1.11","192.168.1.12","192.168.1.13"]]

hosts_list, myIdGroup = getHostList(SERVER_HOSTS_FILE_PATH)
print (hosts_list)
print(myIdGroup)


myLeader = "192.168.1.12"
blockchainPath = "./TT"
toleranceValue = 0.5
voteUmbral = 2

yo = NodoSufAndComis(myHost, 9991, hosts_list, 0, myLeader, toleranceValue, voteUmbral, blockchainPath)




        


