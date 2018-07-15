from block import *

votos = ["voto1", "voto2", "voto3", "voto4"]

bloque = Block()
bloque.createBlock(votos, "init")
hh = bloque.blockHash
print(hh)
print(bloque.verifyBlock(hh))
bloque.addBlockToChain("Test")



