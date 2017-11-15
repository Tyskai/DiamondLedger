# Consensus class
# It takes the transaction pool and forms a candidate block a number of transactions selected from this pool
# Assigns a wait time to all peers who participate on consensus -- Find a trustworty random function
# Choose one peer as leader
# Leader generates the candidate block and sends it to all other participants of consensus process
# if enough number of peers validate the candidate block, it can be declared as valid block and added to the ledger
import hashlib
from Diamond_Ledger import Block


def createHash(message=""):
    return hashlib.sha256(str(message).encode('utf-8')).hexdigest()


class Consensus:

# leader calls this function to create candidate block
    def createCandidateBlock(self,parentHash,transactionPool):
        self.transactions = list()
        for i in range(5):
            if transactionPool.getTransactionPool()[i]["Valid"]:
                self.transactions.append(transactionPool.getTransactionPool()[i]) # Transactions can be validated again
    # get parent hash some where

        block = Block()
        block.newBlock(parentHash,self.transactions)
        #print(block.printBlock())
        return block

# Assign wait times choose the leader
    def findLeader(self,listofPeers):
        pass

    def validateCandidateBlock(self,candidateBlock,chain):
        blockContents = "{0}{1}{2}".format(str(candidateBlock.parentHash),str(candidateBlock.blockOrder),str(candidateBlock.transactions))
        if candidateBlock.blockHash != createHash(blockContents):
            print("Block hash is not match!! Invalid Block!!")
            return False
        if chain[-1].blockHash != candidateBlock.parentHash and chain[-1].blockOrder != candidateBlock.blockOrder - 1:
            print("Parent Hash is not matched!! Invalid Block!!")
            return False
            # check if the transactions are valid
            # if all valid return true
        return True

def addBlock(self,chain,candidateBlock):
        chain.append(candidateBlock)
        # if enough valid votes append ledger

#state = [{"Diamond":"gray","Owner":9876567890,"Valid":True},{"Diamond":"white","Owner":456789078,"Valid":True}]
#b = Block()
#print(b.printBlock())
#c = Consensus()
#c.createCandidateBlock(b.blockHash,state)
