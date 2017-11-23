# Block class
# Creates a block with given features
import hashlib

blockNum=0

def createHash(message=""):
    return hashlib.sha256(str(message).encode('utf-8')).hexdigest()


class Block:

# Create genesis block
    def __init__(self):
        global blockNum
        if blockNum == 0:
            self.parentHash = ""
            self.blockOrder = blockNum
            self.transactions = ""
            self.blockHash = createHash("{0}{1}{2}".format(self.parentHash,str(self.blockOrder),self.transactions))
            blockNum += 1

# Create a new block
    def newBlock(self,parentHash,listOfTransactions):
        global blockNum
        self.parentHash = parentHash
        self.blockOrder = blockNum
        self.transactions = listOfTransactions
        self.blockHash = createHash("{0}{1}{2}".format(self.parentHash,str(self.blockOrder),self.transactions))
        blockNum += 1

    def getBlockHash(self):
        return self.blockHash

# Print block info
    def printBlock(self):
        print("BLOCK nr: {0}\nParent Hash: {1}\nBlock Hash: {2}\n Transactions".format(str(self.blockOrder),self.parentHash,self.blockHash))
        for i in range(len(self.transactions)):
            t = self.transactions[i]
            print("TRANSACTION NUMBER {0} \n Header:{1} \n Diamond{2} \n Current owner: {3} \n Next Owner: {4} \n Valid: {5} \n Signature: {6}".format(i,t["Header"],t["Diamond"].diamondString(),t["Current Owner"], t["Next Owner"], t["Valid"], t["Signature"]))
        print("\n")

    def getTransactions(self):
        return self.transactions

    def getBlockNum(self):
        return self.blockOrder

    #Check if a given diamond exists in a block
    def diamondExists(self, diamondId):
        for t in self.transactions:
            if diamondId == t["Diamond"].getDID():
                return True
        return False

    #Check if a given diamond exists in a block
    def findDiamond(self, diamondId):
        trans = list()
        for t in self.transactions:
            if diamondId == t["Diamond"].getDID():
                trans.append(t)
        return trans

    def findUser(self, userId):
        trans = list()
        for t in self.transactions:
            if userId == t["Current Owner"]:
                trans.append(t)
            elif userId == t["Next Owner"]:
                trans.append(t)
        return trans