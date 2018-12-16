from nodo import *
from random import randint
import sys
import time

SERVER_HOSTS_FILE_PATH = "Conf/serverHosts"

def getHostList(fileName):
    file = open(fileName, 'r')
    ips = []
    groupsIDs = []
    for line in file:
	tokens = line.split(" ")
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

print("Obteniendo hosts...")
hosts_list = getHostList(SERVER_HOSTS_FILE_PATH)
myHost = "192.168.1.7"
newNode = NodoVotante(myHost, 9999)
votes = int(sys.argv[1])
for i in range(0, votes):
    for j in range(0, len(hosts_list)):
        rand = randint(0, len(hosts_list[j]) - 1)
        print("Enviando voto a blockchain " + str(j) + " en " + hosts_list[j][rand])
        newNode.sendVote(j, ".newVotes/Shares" + str(i) + "_" + str(j), hosts_list[j][rand])
    time.sleep(1)


#suffrageNodeHost = "192.168.1.10"

#yo = NodoVotante("192.168.1.7", 9999, suffrageNodeHost)

#for i in range(0,10):
#yo.sendVote(0, "newVote")
