import socket
import threading

MAX_SERVER_SOCKET_CONNECTIONS = 5
MAX_SERVER_SOCKET_MESSAGE_LEN = 8192

NO_CONNECTION = -1
SENDING_SUCCESSFUL = 1

class SocketManager:
	hosts_list = []
	myHost = ""
	port = ""
	serverSocket = 0
	clientSocket = 0
	messageHandler = 0 #Funcion que recibe el mensaje y lo procesa.
	serverSocketThread = 0
	def __init__(self, hosts_list, myHost, port, messageHandler):
		self.hosts_list = hosts_list
		self.myHost = myHost
		self.port = port
		self.messageHandler = messageHandler
		self.clientSocket = 0
		self.serverSocket = 0
		self.serverSocketThread = threading.Thread(target = self.initServerSocket)
		#self.serverSocketThread.setDaemon(True)
		self.serverSocketThread.start()
	def initServerSocket(self):
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.bind(("", self.port))
		self.serverSocket.listen(MAX_SERVER_SOCKET_CONNECTIONS)
		try:
			while True:
				connection, client_address = self.serverSocket.accept()
				try:
					message = connection.recv(MAX_SERVER_SOCKET_MESSAGE_LEN)
					self.messageHandler(message, self)
				finally:
					connection.close()
		finally:
			self.serverSocket.close()
	def sendMessage(self, message, host):
		self.clientSocket = socket.socket()
		try:
			self.clientSocket.connect((host, self.port))
			self.clientSocket.send(message)
		except socket.error as e:
			#print("Sin coneccion")
			return NO_CONNECTION
		finally:
			self.clientSocket.close()
		return SENDING_SUCCESSFUL



