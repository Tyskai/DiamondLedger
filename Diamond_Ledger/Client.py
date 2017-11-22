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

    def validateCandidateBlock(self, candidateBlock, chain,state,publicKey):
        return self.cons.validateCandidateBlock(candidateBlock,chain,state,publicKey)

    def createTransaction(self,diamond, nextOwner):
        transaction = self.trans.createTransaction(diamond,self.keyPair.getAddress(),nextOwner)
        signature = hashlib.sha256(transaction["Header"].encode('utf-8')).hexdigest()  # find a signature algorithm
        transaction["Signature"] = self.keyPair.sign(signature)
        return transaction

    def getAddress(self):
        return self.keyPair.getAddress()

    def getPublicKey(self):
        return self.keyPair.getPublicKey()

    def getPrivateKey(self):
        return self.keyPair.getPrivateKey()

    def queryTransaction(self,id,chain):
        return self.trans.queryDiamond(id,chain)
        pass

    def setKeyPair(self, public, private):
        self.keyPair.setKeyPair(public, private)

# change leader state
    def setLeader(self,bool):
        self.leader = bool
