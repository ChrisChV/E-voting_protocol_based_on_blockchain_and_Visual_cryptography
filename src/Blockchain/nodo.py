from SocketManager import *
import random
import time

TIME_TO_SLEEP_IN_CICLE = 10

SplitDelimitator = ';'
VotingNodeStr = "VotingNode"
SufAndComisStr = "SufAndComisNode"
SufAndComisPoolStr = "SufAndComisPool"
SufAndComisNewLeader = "NewLeader"
SufAndComisDeleteStr = "DeleteVotingPool"
SufAndComisDeleteResStr = "ResDeleteVotingPool"
SufAndComisTrustValuesStr = "TrustValues"
SufAndComisNoticeCandidate = "NoticeCandidate"
SufAndComisVeredict = "Veredict"
SufAndComisVeredictPositive = "Positive"
SufAndComisVeredictNegative = "Negative"
SufAndComisVerifyVote = "VerifyVote"
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
		message += str(random.randint(1,123456))
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
	mutexAuxCount = 0
	mutexVeredicts = 0
	auxCount = 0
	veredicts = {}
	actualVoteId = 0

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
		self.mutexAuxCount = threading.Lock()
		self.mutexVeredicts = threading.Lock()
		self.mutexClycle.acquire()
		self.threadOfCiclo = 0
		self.cicleFlag = False
		self.actualVoteId = 0
		self.auxCount = 0
		veredicts = {}
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
				self.cicleVotingPool = self.votingPool[:]
				self.votingPool = []
				self.mutexVotingPool.release()
				lastVote = splitMessageList[2]
				actualI = 0
				for i in range(len(self.cicleVotingPool) - 1, -1, -1):
					if(lastVote == self.cicleVotingPool[i]):
						actualI = i
						break
				self.mutexVotingPool.acquire()
				for i in range(actualI + 1, len(self.cicleVotingPool)):
					self.votingPool.append(self.cicleVotingPool[-1])
					self.cicleVotingPool = self.cicleVotingPool[:-1]
				self.mutexVotingPool.release()
				message = SufAndComisStr + SplitDelimitator + SufAndComisDeleteResStr
				self.socketManager.sendMessage(message, clientHost)
			elif(splitMessageList[1] == SufAndComisTrustValuesStr):
				print("Trust Values desde " + clientHost)				
				self.trust_values = [float(i) for i in splitMessageList[2].split(SplitTrustValueDelimitator)]
				self.threadOfCiclo = threading.Thread(target = self.startClicle)
				self.threadOfCiclo.start()
			elif(splitMessageList[1] == SufAndComisDeleteResStr):
				print("Respuesta voting Pool desde " + clientHost)
				#auxCount += 1
				#if(auxCount == len(self.hosts_list[self.idGroup]) - 1):
				#	mutexAuxCount.release()
			elif(splitMessageList[1] == SufAndComisVerifyVote):
				print("Orden de verificacion desde " + clientHost)
				self.threadOfCiclo = threading.Thread(target = self.verifyVote, args=(int(splitMessageList[2]),))
				self.threadOfCiclo.start()
			elif(splitMessageList[1] == SufAndComisVeredict):
				print("Veredicto desde " + clientHost)
				self.mutexVeredicts.acquire()
				if(int(splitMessageList[3]) == self.actualVoteId):
					self.veredicts[clientHost] = splitMessageList[2]
				self.mutexVeredicts.release()
			elif(splitMessageList[1] == SufAndComisNoticeCandidate):
				print("Noticia de candidato desde " + clientHost)
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

	def sendNoticeToCandidates(self, candidates):
		message = SufAndComisStr + SplitDelimitator + SufAndComisNoticeCandidate
		self.sendToAllCandidates(message, candidates)

	def sendToAllGroup(self, message):
		for host in self.hosts_list[self.idGroup]:
			if(host != self.socketManager.myHost):
				self.socketManager.sendMessage(message, host)				

	def sendToAllCandidates(self, message, candidates):
		for i in candidates:
			self.socketManager.sendMessage(message, self.hosts_list[self.idGroup][i])			

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
		sumTrustValues = float(sum(self.trust_values))
		for i in range(0, len(self.trust_values)):
			if(self.hosts_list[self.idGroup][i] == self.socketManager.myHost):
				sumTrustValues -= self.trust_values[i]
				break;

		probabilidades = []
		for i in range(0, len(self.trust_values)):
			if(self.hosts_list[self.idGroup][i] == self.socketManager.myHost):
				probabilidades.append(0)
			else:
				probabilidades.append(self.trust_values[i] / sumTrustValues)
		probAcumuladas = []
		actualProb = 0
		for value in probabilidades:
			actualProb += value
			probAcumuladas.append(actualProb)
		probAcumuladas[-1] = 1.0
		candidates = []
		for i in range(0, int(len(self.hosts_list[self.idGroup]) / 2)):
			randNum = random.uniform(0,1)
			for j in range(0, len(probAcumuladas)):
				if(randNum <= probAcumuladas[j]):
					candidates.append(j)
					break;
		return candidates

	def verifyVote(self, voteId):
		#TODO
		print("Verificando voto: " + self.cicleVotingPool[voteId])
		message = SufAndComisStr + SplitDelimitator + SufAndComisVeredict + SplitDelimitator + SufAndComisVeredictPositive + SplitDelimitator + str(voteId)
		self.socketManager.sendMessage(message, self.host_leader)


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
		auxCount = 0
		self.sendDeleteVotingPoolToAllGroup(lastVote)
		candidates = self.choseCandidates()
		print(candidates)
		self.sendNoticeToCandidates(candidates)
		verifiedVotes = self.cicleVerifyVotes(candidates)
		print(verifiedVotes)
		self.waitCicle()


	def cicleVerifyVotes(self, candidates):
		self.actualVoteId = 0
		verifiedVotes = []
		for i in range(0, len(self.cicleVotingPool)):
			message = SufAndComisStr + SplitDelimitator + SufAndComisVerifyVote + SplitDelimitator + str(self.actualVoteId)
			self.sendToAllCandidates(message, candidates)
			time.sleep(TIME_TO_SLEEP_IN_CICLE)
			self.mutexVeredicts.acquire()
			self.actualVoteId  += 1
			self.mutexVeredicts.release()
			positiveVeredicts = 0
			negativeVeredicts = 0
			for cand in candidates:
				host = self.hosts_list[self.idGroup][cand]
				if(host in self.veredicts):
					if(self.veredicts[host] == SufAndComisVeredictPositive):
						positiveVeredicts += 1
					else:
						negativeVeredicts += 1
			mayoria = 0
			if(positiveVeredicts > negativeVeredicts):
				mayoria = SufAndComisVeredictPositive
			elif(positiveVeredicts < negativeVeredicts):
				mayoria = SufAndComisVeredictNegative
			for cand in candidates:
				host = self.hosts_list[self.idGroup][cand]
				if not(host in self.veredicts):
					self.trust_values[cand] *= self.toleranceValue
				elif(self.veredicts[host] != mayoria):
					self.trust_values[cand] *= self.toleranceValue
			if(mayoria == SufAndComisVeredictPositive):
				verifiedVotes.append(self.cicleVotingPool[self.actualVoteId - 1])
		return verifiedVotes






		











