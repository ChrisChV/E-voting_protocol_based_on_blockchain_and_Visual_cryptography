from nodo import *
import time

suffrageNodeHost = "192.168.1.10"

yo = NodoVotante("192.168.1.7", 9999, suffrageNodeHost)

for i in range(0,100):
	print("Mensaje " + str(i) + " enviado")
	yo.sendVote(0, "voteTest1")
	time.sleep(1)




