import sys
from Diamond_Ledger import Diamond, Client

def str2bool(v):
  return v.lower() in ("true", "t", "1")

def searchChainFindDiamond(chain,diamond):
    for i in range(len(chain)):
        if chain[i].diamondExists(diamond):
            return True
    return False

def searchChainFindUserId(chain, userId):
    trans = []
    for i in range(len(chain)):
        trans.append(chain[i].findUser(userId))

def demo(chain, transactionpool, clientlist=[]):
    print("Welcome to Secure Diamonds Trade \nWhat wouly like to do \n  1. Create an account \n  2. Login to your account \n q. to quit the menu")
    awnser = input("Type 1 or 2: ")
    if awnser == "1":
        return newUser(chain, transactionpool)
    elif awnser == "2":
        return login(chain, transactionpool)
    elif awnser == "q":
        print("Goodday")
    else:
        print("Command was not recognised. Try again.")
        return demo(chain, transactionpool, [])
    return (chain, transactionpool, [])

#Allows the user to register and add a diamond to the system
def newUser(chain,pool):
    print("Welcome new user \n Please specify your diamond.")

    dColor = int(input("Diamond color (int): "))
    dClarity = int(input("Diamond clarity: "))
    dCut = int(input("Diamond cut: "))
    dCarat = int(input("Diamond Carat: "))
    dOrigin = input("Diamond country of Origin: ")
    dIsNatural = str2bool(input("Is the diamond natural (True/False) : "))

    diamond = Diamond(dColor,dClarity,dCut,dCarat,dOrigin,dIsNatural)
    if searchChainFindDiamond(chain,diamond):
        print("The diamond is already registered in the chain. Exit")
    else:
        print("The diamond was created succesfully!")
        diamond.printDiamond()

        client = Client()
        transaction = client.createTransaction(diamond,client,pool)
        pool.addTransaction(transaction)
        # Save the keys locally
        writeKeysToFile(client.getPublicKey(), client.getPrivateKey())
        print("Clients public key:")
        print(client.getPublicKey())
        print("(Is also saved in publicKey.txt. \n Private key is saved in privateKey.txt \n We will now send you back to the main menu \n\n")

    return (chain, pool, [client])

def login(chain, pool):
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
        print(searchChainFindUserId(chain,public))
    elif(awnser=="2"):
        print("To whom do you want to do an transaction. TODO ")
    elif(awnser=="q"):
        print("Goodday!")
        return(chain, pool)
    else:
        print("command was not regocnized. Please try again.")
        return (login(chain,pool))
    return (chain, pool, [])

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