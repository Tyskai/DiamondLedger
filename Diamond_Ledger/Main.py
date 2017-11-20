from Diamond_Ledger import Client,State, Consensus, Demo
from Diamond_Ledger import TransactionPool,Diamond,Block
import random

def printChain(chain):
    # Print all the blocks in the chain
    for i in range(len(chain)):
        chain[i].printBlock()

# create genesis block
genesisBlock = Block()
chain = list()
chain.append(genesisBlock)

# create transaction pool. At first it is empty
transactionPool = TransactionPool()

# create 20 clients
clientList = list()
for i in range(21):
    clientList.append(Client())

# initially 25 diamonds
location = ["netherlands","germany","france","spain","poland","finland","swiss"]
diamonds = list()
for j in range(25):
    r = random.randint(1,7)
    diamonds.append(Diamond(r,r,r,r,location[r-1],True))

# Generate a state, which knows for every diamond which client is the owner.
state = State.State()
ownership = list()
for i in range(len(clientList)):
    ownership.append({"Diamond":diamonds[i],"Owner":clientList[i].getPublicKey()})
state.initializeState(ownership)

# Generate 20 valid transactions
for k in range(20):
    clientList[k].createTransaction(diamonds[k],clientList[k+1].getPublicKey(),transactionPool)
    # validate transactions
    transactionPool.validateTransaction(transactionPool.getTransactionPool()[k],state)

# then generate blocks - Mining
# consensus process : choose one of the clients as leader. Leader creates candidate block. If majority of the remaining
# clients ( validators ) validate the candidate block, then it is added to the chain
def mineBlocks(chain, transactionPool, clientList, state):
    cons = Consensus()
    votes = list()
    while len(transactionPool) >= 5:
        leader = cons.findLeader(clientList)
        validators = clientList.copy()
        validators.remove(leader)
        candidateBlock = leader.createCandidateBlock(chain[-1].getBlockHash(),transactionPool)

        # voting the candidate block
        for i in range(len(validators)):
            votes.append(validators[i].validateCandidateBlock(candidateBlock,chain,state))

        if sum(votes) > (len(clientList)/2)+1:
            # Block is voted valid (by at least half + 1 of the clients)
            # Block will be added to the chain
            chain.append(candidateBlock)
            state.updateState(transactionPool)
            transactionPool.removeTransactions()
            leader.setLeader(False)

# Remove one transaction in the pool, so that the new user can add his diamond directly
transactionPool.removeTransactions(1)

mineBlocks(chain, transactionPool, clientList, state)

print("Chain before the Demo starts")
printChain(chain)

# Start demo (do 3 times
for i in range(0,3):
   (c,p,cList) = Demo.demo(chain,transactionPool)
   print("DEMO finished \n Update Chain, transactionPool and Clientlist \n Mine the blocks \n")
   chain = c
   transactionPool = p
   clientList = clientList + cList

   mineBlocks(chain, transactionPool, clientList, state)

   printChain(chain)