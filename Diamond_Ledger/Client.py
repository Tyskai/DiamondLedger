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
        self.leader = False

    def createCandidateBlock(self,parentHash,transactionPool):
        return self.cons.createCandidateBlock(parentHash,transactionPool)

    def validateCandidateBlock(self, candidateBlock, chain,state):
        return self.cons.validateCandidateBlock(candidateBlock,chain,state)

    def createTransaction(self,diamond, nextOwner,pool):
        self.trans.createTransaction(diamond,self.keyPair.getPublicKey(),nextOwner,pool)

    def getPublicKey(self):
        return self.keyPair.getPublicKey()

    def queryTransaction(self,diamond):
        pass

# Assign each client a wait time
# Based on this wait time the leader will be chosen
    def setWaitTime(self):
        pass

# change leader state
    def setLeader(self,):
        pass