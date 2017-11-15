# Client class
# Each client will have a unique key pair
# Each client can create transaction
# Each client is able to participate in consensus
import hashlib
from Diamond_Ledger import Consensus,Diamond,Key,Transaction

class Client:

    def __init__(self):
        self.keyPair = Key()
        self.trans = Transaction()
        #self.diamond = Diamond() # check again
        self.cons = Consensus()

    def createCandidateBlock(self,parentHash,transactionPool):
        return self.cons.createCandidateBlock(parentHash,transactionPool)

    def validateCandidateBlock(self, candidateBlock, chain):
        return self.cons.validateCandidateBlock(candidateBlock,chain)

    def createTransaction(self,diamond, nextOwner,pool):
        self.trans.createTransaction(diamond,self.keyPair.getPublicKey(),nextOwner,pool)

    def getPublicKey(self):
        return self.keyPair.getPublicKey()

    def queryTransaction(self,diamond):
        pass