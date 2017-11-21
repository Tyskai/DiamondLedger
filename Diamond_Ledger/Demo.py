import sys
from Diamond_Ledger import Diamond, Client

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
    print("Welcome to Secure Diamonds Trade \nWhat wouly like to do \n  1. Create an account and add a Diamond \n  2. Login to your account \n q. to quit the menu")
    awnser = input("Type 1 or 2: ")
    if awnser == "1":
        newUser()
    elif awnser == "2":
        login()
    elif awnser == "q":
        print("Goodday")
    else:
        print("Command was not recognised. Try again.")
        demo()
