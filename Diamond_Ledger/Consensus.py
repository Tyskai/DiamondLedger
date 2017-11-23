# Consensus class
# It takes the transaction pool and forms a candidate block a number of transactions selected from this pool
# Assigns a wait time to all peers who participate on consensus -- Find a trustworty random function
# Choose one peer as leader
# Leader generates the candidate block and sends it to all other participants of consensus process
# if enough number of peers validate the candidate block, it can be declared as valid block and added to the ledger
import hashlib, random
from Diamond_Ledger import Block , TransactionPool


def createHash(message=""):
    return hashlib.sha256(str(message).encode('utf-8')).hexdigest()

class Consensus:

# leader calls this function to create candidate block
    def createCandidateBlock(self,parentHash,transactionPool):
        self.transactions = list()
        for i in range(5):

            if transactionPool.getTransactionPool()[i]["Valid"]:
                self.transactions.append(transactionPool.getTransactionPool()[i]) # Transactions can be validated again
            else:
                transactionPool.getTransactionPool()[i]

    # get parent hash some where

        block = Block()
        block.newBlock(parentHash,self.transactions)
        #print(block.printBlock())
        return block

# Assign wait times choose the leader
    def findLeader(self,listofPeers):
        waitTime = list(range(1,len(listofPeers)))
        random.shuffle(waitTime)
        listofPeers[waitTime.index(min(waitTime))].setLeader(True)
        return listofPeers[waitTime.index(min(waitTime))]


    def validateCandidateBlock(self,candidateBlock,chain,state,publicKey):
        transactions = candidateBlock.getTransactions()
        for i in range(len(transactions)):
            clientPublicKey = [item for item in publicKey if item[0] == transactions[i]["Current Owner"]]
            if not TransactionPool.validateTransaction(TransactionPool(),transactions[i],state,clientPublicKey[0][1]):
                print("Transaction is invalidated by verifiers!")
                return False
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
