# Test program
from Diamond_Ledger import Client,State, Consensus
from Diamond_Ledger import TransactionPool,Diamond,Block
import random

cons = Consensus()

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
# initially there are 25 diamonds

location = ["Netherlands","Germany","France","Spain","Poland","Finland","Swiss"]
diamonds = list()
for j in range(25):
    r = random.randint(1,7)
    diamonds.append(Diamond(r,r,r,r,location[r-1],True))

state = State.State()
ownership = list()
for i in range(len(clientList)):
    ownership.append({"Diamond":diamonds[i],"Owner":clientList[i].getPublicKey()})
    #print(initialState[i])

# create transactions

state.initializeState(ownership)
#state.printState()

for k in range(20):
    clientList[k].createTransaction(diamonds[k],clientList[k+1].getPublicKey(),transactionPool)
    # validate transactions
    transactionPool.validateTransaction(transactionPool.getTransactionPool()[k],state)



# then generate blocks
# consensus process : choose one of the clients as leader. Leader creates candidate block. If majority of the remaining
# clients ( validators ) validate the candidate block, then it is added to the chain
votes = list()
while len(transactionPool) != 0:
    leader = cons.findLeader(clientList)
    validators = clientList.copy()
    validators.remove(leader)
    candidateBlock = leader.createCandidateBlock(chain[-1].getBlockHash(),transactionPool)
    #print(candidateBlock.printBlock())

    # voting the candidate block
    for i in range(len(validators)):
        votes.append(validators[i].validateCandidateBlock(candidateBlock,chain,state))

    if sum(votes) > (len(clientList)/2)+1:
        #print("Block is valid!!")
        chain.append(candidateBlock)
        state.updateState(transactionPool)
        transactionPool.removeTransactions()
        leader.setLeader(False)
        #state.printState()

for i in range(len(chain)):
    chain[i].printBlock()
