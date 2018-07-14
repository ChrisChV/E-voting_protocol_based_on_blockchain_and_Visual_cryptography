from network import *

hosts_list = ["123"]

def test(message, net):
	print(message)
	print(net.myHost)

net = Network(hosts_list, "123", 9996, test)
net.sendMessage("Hola amiguito", "25.55.1.76")
print("Done")



