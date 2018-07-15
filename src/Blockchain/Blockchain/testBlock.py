from block import *

#votos = ["voto1", "voto2", "voto3", "voto4"]
votos = ['Credencial1 -> Voto1VS171956', 'Credencial1 -> Voto1VS275760']

bloque = Block()
bloque.createBlock(votos, "Test")
hh = bloque.blockHash
print(hh)
print(bloque.verifyBlock(hh))
bloque.addBlockToChain("Test")



