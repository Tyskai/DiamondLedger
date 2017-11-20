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
        print("Parent Hash: {0}\nBlock Order: {1}\nBlock Hash: {2}\nTransactions".format(self.parentHash,str(self.blockOrder),self.blockHash))
        for i in range(len(self.transactions)):
            print("{0}.{1}".format(i,self.transactions[i]))
        print("\n")

    def getTransactions(self):
        return self.transactions

    def getBlockNum(self):
        return self.blockOrder

    #Check if a given diamond exists in a block
    def diamondExists(self, diamond):
        for t in self.transactions:
            if diamond == t["Diamond"]:
                return True
        return False

    def findUser(self, userId):
        trans = []
        for t in self.transactions:
            if userId == t["Current Owner"]:
                trans = trans.append(t)
                print("hi")
            elif userId == t["Next Owner"]:
                trans = trans.append(t)
                print("hi")
        return trans

#b = Block()
#print(b.printBlock())

#b2 = Block()
#b2.newBlock(b.blockHash,[{"Diamond":"","Owner":1234565432}])
#print(b2.printBlock())

#b3 = Block()
#b3.newBlock(b2.blockHash,[{"Diamond":"pnk","Owner":456789789}])
#print(b3.printBlock())
