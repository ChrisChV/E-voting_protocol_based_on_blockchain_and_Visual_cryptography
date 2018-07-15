from hash import *
import time

BlockSplitDelimiator = ":"
BlockChainConfFileName = "blockchainConf"
BlockChainConfInitBlock = "init"
BLOCK_ACCEPTED = 1
BLOCK_REJECTED = 0

def getLastBlock(pathToBlockchain):
	blockchainConfFile = open(pathToBlockchain + "/" + BlockChainConfFileName, 'r')
	initBlock = blockchainConfFile.readline().rstrip('\n')
	lastBlock = blockchainConfFile.readline().rstrip('\n')
	blockchainConfFile.close()
	return lastBlock

class Block:
	blockHash = ""
	votes = []
	parentHash = ""
	timestamp = ""
	def __init__(self):
		self.blockHash = ""
		self.votes = []
		self.parentHash = ""
		self.timestamp = ""
	def generateData(self):
		data = ""
		for vote in self.votes:
			data += vote + BlockSplitDelimiator
		data += self.parentHash
		return data
	def createBlock(self, voteList, pathToBlockchain):
		self.votes = voteList[:]
		self.parentHash = getLastBlock(pathToBlockchain)
		self.timestamp = str(time.time())
		data = self.generateData()
		self.blockHash = getHash(data)
	def verifyBlock(self, verifyHash):
		if(self.blockHash == verifyHash):
			return BLOCK_ACCEPTED
		return BLOCK_REJECTED
	def addBlockToChain(self, pathToBlockchain):
		blockchainConfFile = open(pathToBlockchain + "/" + BlockChainConfFileName, 'r')
		initBlock = blockchainConfFile.readline().rstrip('\n')
		lastBlock = blockchainConfFile.readline().rstrip('\n')
		numberOfBlocks = int(blockchainConfFile.readline().rstrip('\n')) + 1
		numberOfVotes = int(blockchainConfFile.readline().rstrip('\n')) + len(self.votes)
		blockchainConfFile.close()
		blockchainConfFile = open(pathToBlockchain + "/" + BlockChainConfFileName, 'w')
		if(initBlock == BlockChainConfInitBlock):
			blockchainConfFile.write(self.blockHash + '\n')	
		else:
			blockchainConfFile.write(initBlock + '\n')
		blockchainConfFile.write(self.blockHash + '\n')
		blockchainConfFile.write(str(numberOfBlocks) + '\n')
		blockchainConfFile.write(str(numberOfVotes) + '\n')	
		blockchainConfFile.close()
		newBlock = open(pathToBlockchain + "/" + self.blockHash, 'w')
		newBlock.write(self.blockHash + "\n")
		for vote in self.votes:
			newBlock.write(vote + '\n')
		newBlock.write(self.parentHash + '\n')
		newBlock.write(self.timestamp + '\n')
		newBlock.close()



		
	

