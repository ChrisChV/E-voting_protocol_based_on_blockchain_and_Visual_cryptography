from nodo import *

suffrageNodeHost = "192.168.1.10"

yo = NodoVotante("192.168.1.7", 9999, suffrageNodeHost)

#for i in range(0,10):
yo.sendVote(0, "newVote")