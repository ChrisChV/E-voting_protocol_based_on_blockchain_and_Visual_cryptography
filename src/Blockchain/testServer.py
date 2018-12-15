from nodo import *
import sys;


SERVER_HOSTS_FILE_PATH = "../Conf/serverHosts"


def getHostList(fileName):
    file = open(fileName, 'r')
    ips = []
    groupsIDs = []
    for line in file:
        tokens = line.split(" ")
        print(tokens)
        ips.append(tokens[1])
        groupsIDs.append(int(tokens[3].strip('\n')))
    hosts_list = []
    numOfGroups = max(groupsIDs) + 1
    for i in range(0, numOfGroups):
        hosts_list.append([])
    for i in range(0, len(ips)):
        hosts_list[groupsIDs[i]].append(ips[i])
    file.close()
    return hosts_list




#hosts_list = [["192.168.1.10", "192.168.1.11","192.168.1.12","192.168.1.13"]]

hosts_list = getHostList(SERVER_HOSTS_FILE_PATH)
print (hosts_list)



myHost = "192.168.1.12"
myLeader = "192.168.1.12"
blockchainPath = "./TT"
toleranceValue = 0.5
voteUmbral = 2

yo = NodoSufAndComis(myHost, 9991, hosts_list, 0, myLeader, toleranceValue, voteUmbral, blockchainPath)




        


