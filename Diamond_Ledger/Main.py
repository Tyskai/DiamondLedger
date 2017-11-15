# Test program
from Diamond_Ledger import Client
from Diamond_Ledger import TransactionPool,Diamond,Block
import random

# create genesis block
genesisBlock = Block()
chain = list()
chain.append(genesisBlock)

# create transaction pool. at first is empty
transactionPool = TransactionPool()

# create clients
clientList = list()
for i in range(21):
    clientList.append(Client())

# define initial state ( ownership )
# initially there are 6 diamonds

location = ["Netherlands","Germany","France","Spain","Polland","Finland","Swiss"]
diamonds = list()
for j in range(25):
    r = random.randint(1,7)
    diamonds.append(Diamond(r,r,r,r,location[r-1],True))

initialState = list()
for i in range(len(clientList)):
    initialState.append({"Diamond":diamonds[i%6],"Owner":clientList[i].getPublicKey()})
    #print(initialState[i])
# create transactions
for k in range(20):
    clientList[k].createTransaction(diamonds[k%6],clientList[k+1].getPublicKey(),transactionPool)
    # update state


# validate transactions

# then generate blocks
# consensus process : choose one of the clients as leader. Leader creates candidate block. If majority of the remaining
# clients ( validators ) validate the candidate block, then it is added to the chain
votes = list()
while len(transactionPool) != 0:
    leader = clientList[random.randint(0, 20)]
    validators = clientList.copy()
    validators.remove(leader)
    candidateBlock = leader.createCandidateBlock(chain[-1].getBlockHash(),transactionPool)
    #print(candidateBlock.printBlock())

    # voting the candidate block
    for i in range(len(validators)):
        votes.append(validators[i].validateCandidateBlock(candidateBlock,chain))

    if sum(votes) > (len(clientList)/2)+1:
        #print("Block is valid!!")
        chain.append(candidateBlock)
        transactionPool.removeTransactions()

for i in range(len(chain)):
    chain[i].printBlock()