from SocketManager import *
import random

SplitDelimitator = ';'
VotingNodeStr = "VotingNode"
SufAndComisStr = "SufAndComisNode"
SufAndComisPoolStr = "SufAndComisPool"
SufAndComisNewLeader = "NewLeader"
SufAndComisDeleteStr = "DeleteVotingPool"
SufAndComisTrustValuesStr = "TrustValues"
SplitTrustValueDelimitator = ":"
PingStr = "Ping"

#TODO poner mutex para el votingPool

class Nodo:
	socketManager = 0
	def __init__(self, host, port, messageHandler):
		self.socketManager = SocketManager(host, port, messageHandler)


class NodoVotante(Nodo):
	suffrageNodeHost = ""
	def __init__(self, host, port, suffrageNodeHost):
		Nodo.__init__(self, host, port, self.messageHandlerFunction)
		self.suffrageNodeHost = suffrageNodeHost

	def messageHandlerFunction(self, message, clientHost):
		print(message)

	def sendVote(self, blockChainID, voteFileName):
		message = VotingNodeStr + SplitDelimitator + str(blockChainID) + SplitDelimitator
		voteFile = open(voteFileName, 'r')
		vote = voteFile.readline()
		voteFile.close()
		message += vote.rstrip('\n')
		res = self.socketManager.sendMessage(message, self.suffrageNodeHost)
		if(res == NO_CONNECTION):
			print(self.socketManager.myHost + ": No hay coneccion al nodo de sufragio " + self.suffrageNodeHost)
		return res


class NodoSufAndComis(Nodo):
	hosts_list = [] #Lista de listas de los host de cada nodo dividido en grupos
	trust_values = []
	host_leader = ""
	idGroup = 0
	actualBlock = 0
	votingPool = []
	cicleVotingPool = []
	toleranceValue = 0
	voteUmbral = 0
	threadOfCiclo = 0
	mutexClycle = 0
	mutexVotingPool = 0
	cicleFlag = False #Con esto se ve si hay ciclo activo
	def __init__(self, host, port, hosts_list, idGroup, initLeader, toleranceValue, voteUmbral):
		Nodo.__init__(self, host, port, self.messageHandlerFunction)
		self.hosts_list = hosts_list
		self.idGroup = idGroup
		self.actualBlock = 0
		self.host_leader = initLeader
		self.votingPool = []
		self.cicleVotingPool = []
		self.toleranceValue = toleranceValue
		self.voteUmbral = voteUmbral
		self.mutexClycle = threading.Lock()
		self.mutexVotingPool = threading.Lock()
		self.mutexClycle.acquire()
		self.threadOfCiclo = 0
		self.cicleFlag = False
		if(host == initLeader):
			self.threadOfCiclo = threading.Thread(target = self.waitCicle)
			self.threadOfCiclo.start()
			self.trust_values = [1.0] * len(hosts_list[self.idGroup])

	def messageHandlerFunction(self, message, clientHost):
		splitMessageList = message.split(SplitDelimitator)
		if(splitMessageList[0] == VotingNodeStr):
			print("Nuevo voto desde " + clientHost + " :" + splitMessageList[2])
			self.sendVotingToAllGroup(splitMessageList[2], int(splitMessageList[1]))
			self.socketManager.sendMessage("Voto recibido", clientHost)
		elif(splitMessageList[0] == SufAndComisStr):
			if(splitMessageList[1] == SufAndComisPoolStr):
				self.mutexVotingPool.acquire()
				self.votingPool.append(splitMessageList[2])
				self.mutexVotingPool.release()
				print("Nuevo voto desde " + clientHost + " :" + splitMessageList[2])
				if(self.socketManager.myHost == self.host_leader and self.cicleFlag == False and len(self.votingPool) >= self.voteUmbral):
					self.cicleFlag = True
					self.mutexClycle.release()
			elif(splitMessageList[1] == SufAndComisNewLeader):
				if(clientHost == self.host_leader):
					self.host_leader = splitMessageList[2]
					print("Nuevo lider escogido: " + self.host_leader)
			elif(splitMessageList[1] == SufAndComisDeleteStr):
				print("Eliminar voting Pool desde " + clientHost)
				self.mutexVotingPool.acquire()
				votingPoolCopy = self.votingPool[:]
				self.votingPool = []
				self.mutexVotingPool.release()
				lastVote = splitMessageList[2]
				actualI = 0
				for i in range(len(votingPoolCopy) - 1, -1, -1):
					if(lastVote == votingPoolCopy[i]):
						actualI = i
						break
				self.mutexVotingPool.acquire()
				for i in range(actualI + 1, len(votingPoolCopy)):
					self.votingPool.append(votingPoolCopy[i])
				self.mutexVotingPool.release()
			elif(splitMessageList[1] == SufAndComisTrustValuesStr):
				print("Trust Values desde " + clientHost)				
				self.trust_values = [float(i) for i in splitMessageList[2].split(SplitTrustValueDelimitator)]
				self.threadOfCiclo = threading.Thread(target = self.startClicle)
				self.threadOfCiclo.start()
			elif(splitMessageList[1] == PingStr):
				print("Ping desde " + clientHost)
			else:
				print(message)
		

	def pingToNode(self, host):
		message = SufAndComisStr + SplitDelimitator + PingStr;
		print("Ping a " + host)
		return self.socketManager.sendMessage(message, host)

	def sendVotingToAllGroup(self, vote, idGroup):
		message = SufAndComisStr + SplitDelimitator + SufAndComisPoolStr + SplitDelimitator + vote
		for host in self.hosts_list[idGroup]:
			if(host == self.socketManager.myHost):
				self.mutexVotingPool.acquire()
				self.votingPool.append(vote)
				self.mutexVotingPool.release()
				if(host == self.host_leader and self.cicleFlag == False and len(self.votingPool) >= self.voteUmbral):
					self.cicleFlag = True
					self.mutexClycle.release()
			else:
				self.socketManager.sendMessage(message, host)


	def sendNewLeaderToAllGroup(self, newLeader):
		message = SufAndComisStr + SplitDelimitator + SufAndComisNewLeader + SplitDelimitator + newLeader
		self.sendToAllGroup(message)

	def sendDeleteVotingPoolToAllGroup(self, lastVote):
		message = SufAndComisStr + SplitDelimitator + SufAndComisDeleteStr + SplitDelimitator + lastVote
		self.sendToAllGroup(message)

	def sendToAllGroup(self, message):
		for host in self.hosts_list[self.idGroup]:
			if(host != self.socketManager.myHost):
				self.socketManager.sendMessage(message, host)				

	def choseLeader(self):
		res = NO_CONNECTION
		newLeader = ""
		while res == NO_CONNECTION:
			randNum = random.randint(0, len(self.hosts_list[self.idGroup]))
			newLeader = self.hosts_list[self.idGroup][randNum % len(self.hosts_list[self.idGroup])]
			if(newLeader == self.socketManager.myHost):
				newLeader = self.hosts_list[self.idGroup][(randNum + 1) % len(self.hosts_list[self.idGroup])]
			res = self.pingToNode(newLeader)
		self.sendNewLeaderToAllGroup(newLeader)
		self.host_leader = newLeader
		trustValuesStr = ""
		for i in range(0, len(self.trust_values)):
			trustValuesStr += str(self.trust_values[i])
			if(i != len(self.trust_values) - 1):
				trustValuesStr += SplitTrustValueDelimitator

		message = SufAndComisStr + SplitDelimitator + SufAndComisTrustValuesStr + SplitDelimitator + trustValuesStr
		self.socketManager.sendMessage(message, newLeader)
		print("Nuevo lider escogido: " + newLeader)
	
	def choseCandidates(self):
		probabilidades = []


	def waitCicle(self):
		self.mutexClycle.acquire()
		self.choseLeader();
		self.cicleFlag = False

	def startClicle(self):
		print("Ciclo Iniciado")
		print(self.trust_values)
		self.mutexVotingPool.acquire()
		lastVote = self.votingPool[-1]
		self.cicleVotingPool = self.votingPool[:]
		self.votingPool = []
		self.mutexVotingPool.release()
		print(self.cicleVotingPool)
		self.sendDeleteVotingPoolToAllGroup(lastVote)
		self.waitCicle()
		



		











