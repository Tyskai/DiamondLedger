from Diamond_Ledger import Client,State, Consensus, Demo
from Diamond_Ledger import TransactionPool,Diamond,Block
import random

### Functions needed for the Demo

def str2bool(v):
  return v.lower() in ("true", "t", "1")

# go through the chain, find a given diamond
def searchChainFindDiamond(diamond):
    global chain
    for i in range(len(chain)):
        if chain[i].diamondExists(diamond):
            return True
    return False

# go though the chain, find a user Id and all his done/received transactions
def searchChainFindUserId(userId):
    global chain
    trans = []
    for i in range(len(chain)):
        trans.append(chain[i].findUser(userId))

# Allows the user to register and add a diamond to the system
def newUser():
    global chain, transactionPool
    print("Welcome new user \n Please specify your diamond.")

    dColor = int(input("Diamond color (int): "))
    dClarity = int(input("Diamond clarity: "))
    dCut = int(input("Diamond cut: "))
    dCarat = int(input("Diamond Carat: "))
    dOrigin = input("Diamond country of Origin: ")
    dIsNatural = str2bool(input("Is the diamond natural (True/False) : "))

    diamond = Diamond(dColor,dClarity,dCut,dCarat,dOrigin,dIsNatural)
    if searchChainFindDiamond(diamond):
        print("The diamond is already registered in the chain. Exit")
        return(chain, transactionPool, [])
    else:
        print("The diamond was created succesfully!")
        diamond.printDiamond()

        client = Client()
        transaction = client.createTransaction(diamond,client.getPublicKey())
        transactionPool.addTransaction(transaction)
        # Save the keys locally
        writeKeysToFile(client.getPublicKey(), client.getPrivateKey())
        print("Clients public key:")
        print(client.getPublicKey())
        print("(Is also saved in publicKey.txt. \n Private key is saved in privateKey.txt \n We will now send you back to the main menu \n\n")


# Client loges in and can either see his transactions or do a transaction
def login():
    global chain
    #Read the public and private key from the files
    #recreate the client with those keys
    print("Read public and private key from file")
    client = Client()
    public, private = readKeysFromFile()
    client.setKeyPair(public, private)

    print("Client is recognized, client public key is:")
    print(public)
    print("What do you want to do \n 1. See your transactions \n 2. Do transaction \n q. quit")
    awnser = input("Type 1 or 2: ")
    if(awnser=="1"):
        print("Your transactions are:")
        print(searchChainFindUserId(public))
    elif(awnser=="2"):
        print("To whom do you want to do an transaction. TODO ")
    elif(awnser=="q"):
        print("Goodday!")
    else:
        print("command was not regocnized. Please try again.")
        login()

def readKeysFromFile():
    text_file = open("publicKey.txt", "r")
    publicKey = text_file.read()
    text_file.close()
    text_file = open("privateKey.txt", "r")
    privateKey = text_file.read()
    text_file.close()
    return (publicKey, privateKey)

def writeKeysToFile(public, private):
    text_file = open("publicKey.txt", "w")
    text_file.write(public)
    text_file.close()
    text_file = open("privateKey.txt", "w")
    text_file.write(private)
    text_file.close()

# start the demo, user can either, create an acoount, or login
def demo():
    global chain, transactionPool, ClientList
    print("Welcome to Secure Diamonds Trade \nWhat wouly like to do \n  1. Create an account and add a Diamond \n  2. Login to your account \n chain. See the current chain. \n pool. See the transaction pool")
    awnser = input("Type 1 or 2: ")
    if awnser == "1":
        newUser()
    elif awnser == "2":
        login()
    elif awnser == "q":
        print("Goodday")
    elif awnser == "chain":
        print(chain)
    elif awnser == "pool":
        print(transactionPool.printPool())
    else:
        print("Command was not recognised. Try again.")
        demo()

### Functions

def printChain():
    global chain
    # Print all the blocks in the chain
    for i in range(len(chain)):
        chain[i].printBlock()

### Begin file

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
    transaction = clientList[k].createTransaction(diamonds[k],clientList[k+1].getPublicKey())
    # validate transactions
    transactionPool.addTransaction(transaction)
    transactionPool.validateTransaction(transactionPool.getTransactionPool()[k],state)

# then generate blocks - Mining
# consensus process : choose one of the clients as leader. Leader creates candidate block. If majority of the remaining
# clients ( validators ) validate the candidate block, then it is added to the chain
def mineBlocks():
    global chain, transactionPool, clientList, state

    cons = Consensus()
    votes = list()
    transactionPool.validateTransactionS(state)

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

print(transactionPool.printPool())
mineBlocks()

print("Chain before the Demo starts")
printChain()

print("Pool before start")
print(transactionPool.printPool())

# Start demo (do 3 times
for i in range(0,3):
   demo()
   print("DEMO finished \n Update Chain, transactionPool and Clientlist \n Mine the blocks \n")

   mineBlocks()



