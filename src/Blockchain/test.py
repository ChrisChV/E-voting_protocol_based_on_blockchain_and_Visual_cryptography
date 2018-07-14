from nodo import *

suffrageNodeHost = "25.11.187.246"

yo = NodoVotante("25.55.1.76", 9992, suffrageNodeHost)

yo.sendVote(0, "voteTest1")
yo.sendVote(0, "voteTest2")




