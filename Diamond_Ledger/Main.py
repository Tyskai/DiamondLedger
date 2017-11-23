import itertools
from Diamond_Ledger import Client,State, Consensus
from Diamond_Ledger import TransactionPool,Diamond,Block
import random
from ast import literal_eval as make_tuple

### Functions needed for the Demo

def str2bool(v):
  return v.lower() in ("true", "t", "1")

# go through the chain, find a given diamond
def searchChainFindDiamond(diamondId):
    global chain, transactionPool
    # Search the chain
    for i in range(len(chain)):
        if chain[i].diamondExists(diamondId):
            return True
    # Search the transactionPool
    if(transactionPool.diamondExists(diamondId)):
        return True
    return False

def searchChainFindDiamondHistory(diamondId):
    global chain
    trans = list()
    for i in range(len(chain)):
        trans.append(chain[i].findDiamond(diamondId))
    merge = list(itertools.chain.from_iterable(trans))
    return merge

# go though the chain, find a user Id and all his done/received transactions
def searchChainFindUserId(userId):
    global chain
    trans = list()
    for i in range(len(chain)):
        trans.append(chain[i].findUser(userId))
    merge = list(itertools.chain.from_iterable(trans))
    return merge

def printList(list):
    for i in list:
        print(i)

# Create a diamond
def createDiamond():
    print("Please specify your diamond")
    try:
        dColor = int(input("Diamond color (int): "))
        dClarity = int(input("Diamond clarity: "))
        dCut = int(input("Diamond cut: "))
        dCarat = int(input("Diamond Carat: "))
        dOrigin = input("Diamond country of Origin: ")
        dIsNatural = str2bool(input("Is the diamond natural (True/False) : "))
        diamond = Diamond(dColor, dClarity, dCut, dCarat, dOrigin, dIsNatural)
    except:
        print("Input was not recognized correctly. Color, Clarity, Cut and Carat should be intergeters, Origin should be a text string. Is Natural should be either 'true' or 'false'")
        return (False, None)
    if searchChainFindDiamond(diamond.getDID()):
        print("The diamond is already registered in the chain or transactionPool. Exit.")
        return (False, None)
    else:
        print("The diamond was created succesfully!")
        diamond.printDiamond()
        return (True, diamond)

# Allows the user to register and add a diamond to the system
def newUser():
    global chain, transactionPool
    print("Welcome new user")

    (goon, diamond) = createDiamond()
    if(goon):
        client = Client()
        transaction = client.createTransaction(diamond,client.getAddress())
        transactionPool.addTransaction(transaction)
        clientList.append(client)
        print("Your transaction is:")
        print(transaction)
        # Save the keys locally
        writeKeysToFile(client.getPublicKey(), client.getPrivateKey())
        clientKey.append((client.getAddress(),client.getPublicKey()))
        print("Clients public key:")
        print(client.getPublicKey())
        print("Public and private keys saved in files")
        print("Your address is:")
        print(client.getAddress())

def hackADiamond(client):
    print("hackhack")
    diamondsYouHave = list()
    diamondsIDsYouhave = list()
    s = state.getState()
    indices = [i for i in state.getState() if i["Owner"] == client.getAddress()]
    for j in indices:
        diamondsYouHave.append(j["Diamond"])
        diamondsIDsYouhave.append(j["Diamond"].getDID())
    # Print the diamonds you own
    if len(diamondsYouHave) == 0:
        print("Currently you do not own any diamond.")
    else:
        for i in range(len(diamondsYouHave)):
            print("The diamonds you own are: ")
            print(diamondsYouHave[i].printDiamond())
    print("Please specify your FAULTY diamond (you can improve it)")
    try:
        dColor = int(input("Diamond color (int): "))
        dClarity = int(input("Diamond clarity: "))
        dCut = int(input("Diamond cut: "))
        dCarat = int(input("Diamond Carat: "))
        dOrigin = input("Diamond country of Origin: ")
        dIsNatural = str2bool(input("Is the diamond natural (True/False) : "))
        diamond = Diamond(dColor, dClarity, dCut, dCarat, dOrigin, dIsNatural)
        changeID = input("Alter ID to one of your existing diamonds: ")
        if str2bool(changeID):
            dID = int(input("DiamondID: "))
            diamond.setDID(dID)
    except:
        print("Input was not recognized correctly. Color, Clarity, Cut and Carat should be intergeters, Origin should be a text string. Is Natural should be either 'true' or 'false'")
    print("The FAULTY diamond was created succesfully!")
    diamond.printDiamond()

    # Do a invaldit transaction
    print("Specify your INVALID transaction")
    newOwner = input("Give diamond to (public adres): ")
    transaction = client.createTransaction(diamond,newOwner)
    transactionPool.addTransaction(transaction)
    print("Transaction succesfully added")

# Hack a transaction
def hackATransaction(client):
    global transactionPool
    print("hackhack")

    trans = transactionPool.getLastTransaction()
    transactionPool.removeLastTransaction()
    print("Tamper with transaction:")
    printList(trans)

    trans["Next Owner"] = client.getAddress()
    transactionPool.addTransaction(trans)

    print("Transaction added to the pool")
    print(trans)


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
    print("{} {}".format(public[0],public[1]))
    print("What do you want to do \n 1. See your transactions \n 2. Do transaction \n 3. To add another Diamond \n 4. Trace a diamond \n q. quit")
    awnser = input("Type 1 or 2: ")
    if(awnser=="1"):
        print("Your transactions are:")
        printList(searchChainFindUserId(client.getAddress()))
    elif(awnser=="2"):
        print("To whom do you want to do an transaction. ")
        diamondsYouHave= list()
        diamondsIDsYouhave = list()
        s = state.getState()
        indices = [i for i in state.getState() if i["Owner"] == client.getAddress()]
        for j in indices:
            diamondsYouHave.append(j["Diamond"])
            diamondsIDsYouhave.append(j["Diamond"].getDID())
        # Print the diamonds you own
        if len(diamondsYouHave) == 0:
            print("Currently you do not own any diamond.")
        else:
            for i in range(len(diamondsYouHave)):
                print("The diamonds you own are: ")
                print(diamondsYouHave[i].printDiamond())
        while True:
            receiver = input("Enter receiver's address: ")
            if receiver == client.getAddress():
                print("You cannot transfer diamond to yourself")
            #if[ k for k in range(len(clientList)) if receiver != clientList[k].getAddress() and k == len(clientList)]:
            indice = [k for k in clientList if k.getAddress() == receiver]
            if not indice:
                    print("Receiver's address is not valid")
            if receiver == "quit":
                break
            else:
                break
        diamondID = input("Enter the id of the diamond you want to transfer: ")
        if (diamondID in diamondsIDsYouhave):
            diamondToSend = next(obj for obj in diamondsYouHave if obj.getDID() == diamondID)
            newTransaction = client.createTransaction(diamondToSend, receiver)
            print("We created a new transaction. The following transaction will be added to the pool:")
            print(newTransaction)
            transactionPool.addTransaction(newTransaction)
        else:
            print("You do not own that diamond, and thus can not transfer it.")

    elif(awnser=="3"):
        print("You want to add another diamond.")
        (goon, diamond) = createDiamond()
        if(goon):
            transaction = client.createTransaction(diamond, client.getAddress())
            transactionPool.addTransaction(transaction)
    elif(awnser=="4"):
        print("Search for a diamond in the chain.")
        id = input("Specify diamond id:")
        print("Found diamonds are: ")
        printList(searchChainFindDiamondHistory(id))
    elif(awnser=="q"):
        print("Goodday!")

    elif(awnser=="hack"):
        print("Create a faulty diamond and do a faulty transaction")
        hackADiamond(client)

    elif(awnser =="hack2"):
        print("Hack a transaction in the transaction pool")
        hackATransaction(client)
    else:
        print("command was not regocnized. Please try again.")
        login()

def readKeysFromFile():
    text_file = open("publicKey.txt", "r")
    publicKey = make_tuple(text_file.read())
    text_file.close()
    text_file = open("privateKey.txt", "r")
    privateKey = int(text_file.read())
    text_file.close()
    return (publicKey, privateKey)

def writeKeysToFile(public, private):
    print(public)
    text_file = open("publicKey.txt", "w")
    text_file.write(''.join('{0},{1}'.format(public[0],public[1])))
    text_file.close()
    text_file = open("privateKey.txt", "w")
    text_file.write(private)
    text_file.close()

# start the demo, user can either, create an acoount, or login
def demo():
    global chain, transactionPool, ClientList
    print("DIAMONDS ARE A GIRL'S BEST FRIEND \n A secure diamond trace system \nWhat wouly like to do \n  1. Create an account and add a Diamond \n  2. Login to your account \n chain. See the current chain. \n pool. See the transaction pool \n mine. Mine the pool \n addRandom. To make another user do a random transaction")
    awnser = input(": ")
    if awnser == "1":
        newUser()
    elif awnser == "2":
        login()
    elif awnser == "q":
        print("Goodday")
    elif awnser == "chain":
        printChain()
    elif awnser == "pool":
        transactionPool.printPool()
    elif awnser == "mine":
        mineBlocks()
    elif awnser == "addRandom":
        makeRandomTransaction()
    else:
        print("Command was not recognised. Try again.")
        demo()

def printChain():
    global chain
    # Print all the blocks in the chain
    for i in range(len(chain)):
        chain[i].printBlock()

### Initialize the date to fill the chain
def initilizeChain():
    global chain, transactionPool, clientList, state, clientKey
    # create genesis block
    genesisBlock = Block()
    chain.append(genesisBlock)

    # The number of times to do something
    n = 7

    # create n+1 clients
    for i in range(n+1):
        clientList.append(Client())

    # Add the client public address
    for i in range(len(clientList)):
        clientKey.append((clientList[i].getAddress(),clientList[i].getPublicKey()))

    # initially 25 diamonds
    location = ["netherlands","germany","france","spain","poland","finland","swiss"]
    diamonds = list()
    for j in range(n):
        r = random.randint(1,7)
        diamonds.append(Diamond(j,j,j,j,location[r-1],True))

    # Generate a state, which knows for every diamond which client is the owner.

    ownership = list()
    for i in range(len(clientList)-1):
        ownership.append({"Diamond":diamonds[i],"Owner":clientList[i].getAddress()})
        # add the valid (ownership) transaction to the pool
        transaction = clientList[i].createTransaction(diamonds[i],clientList[i].getAddress())
        transactionPool.addTransaction(transaction)

    # Add all this generated ownerships to the state
    state.initializeState(ownership)

    # Generate n valid transactions
    for k in range(n):
        transaction = clientList[k].createTransaction(diamonds[k],clientList[k+1].getAddress())
        # validate transactions
        transactionPool.addTransaction(transaction)
        clientPublicKey = [item for item in clientKey if item[0] == clientList[k].getAddress()]
        transactionPool.validateTransaction(transactionPool.getTransactionPool()[k],state,clientPublicKey[0][1])

randomTransactionCounter = 1

def makeRandomTransaction():
    global randomTransactionCounter
    global state
    client = Client()
    clientKey.append((client.getAddress(),client.getPublicKey()))
    j = randomTransactionCounter
    r = random.randint(1, 6)
    location = ["netherlands", "germany", "france", "spain", "poland", "finland", "swiss"]
    diamond = Diamond(j, j + 1, j + 4, j + 9, location[r - 1], True)
    transaction = client.createTransaction(diamond, client.getAddress())
    transactionPool.addTransaction(transaction)
    transaction = client.createTransaction(diamond, clientList[r].getAddress())
    transactionPool.addTransaction(transaction)
    randomTransactionCounter =+ 1

# then generate blocks - Mining
# consensus process : choose one of the clients as leader. Leader creates candidate block. If majority of the remaining
# clients ( validators ) validate the candidate block, then it is added to the chain
def mineBlocks():
    global chain, transactionPool, clientList, state, clientKey

    cons = Consensus()
    votes = list()

    #Check the transaction pool for valid transactions, remove the invalide ones
    transactionPool.validateTransactionS(state,clientKey)
    transactionPool.removeInvalidTransactions() #= [m for m in transactionPool.getTransactionPool() if m["Valid"] == True]

    while len(transactionPool) >= 5:
        print("Mining block....")

        leader = cons.findLeader(clientList)
        validators = clientList.copy()
        validators.remove(leader)
        candidateBlock = leader.createCandidateBlock(chain[-1].getBlockHash(),transactionPool)

        # voting the candidate block
        for i in range(len(validators)):
            votes.append(validators[i].validateCandidateBlock(candidateBlock,chain,state,clientKey))

        if sum(votes) > (len(clientList)/2)+1:
            # Block is voted valid (by at least half + 1 of the clients)
            # Block will be added to the chain
            chain.append(candidateBlock)
            state.updateState(transactionPool)
            transactionPool.removeTransactions()
            #validTransactions = [m for m in transactionPool.getTransactionPool() if m["Valid"] == True]
            leader.setLeader(False)


######### Start of the code

#Create the chain
chain = list()
# create transaction pool. At first it is empty
transactionPool = TransactionPool()
# Keep track of the state
state = State()
# Create a list of clients
clientList = list()
# List of Client Address
clientKey = list()

# Generate an inital chain
initilizeChain()

#Mine the first blocks
mineBlocks()

# Start demo
for i in range(0,50):
   print("\n\n DEMO \n\n")
   demo()



