import sys
from Diamond_Ledger import Diamond, Client

def str2bool(v):
  return v.lower() in ("true", "t", "1")

def searchChainFindDiamond(chain,diamond):
    for i in range(len(chain)):
        if chain[i].diamondExists(diamond):
            return True
    return False

def demo(chain, transactionpool):
    print("Welcome to Secure Diamonds Trade \nWhat wouly like to do \n  1. Create an account \n  2. Login to your account \n q. to quit the menu")
    awnser = input("Type 1 or 2: ")
    if awnser == "1":
        return newUser(chain, transactionpool)
    elif awnser == "2":
        print("LOGIN")
    elif awnser == "q":
        print("Goodday")
    else:
        print("Command was not recognised. Try again.")
        return demo(chain, transactionpool)
    return (chain, transactionpool)

#Allows the user to register and add a diamond to the system
def newUser(chain,pool):
    print("Welcome new user")
    name = input("Enter name: ")

    print("Please specify your diamond.")

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
        client.createTransaction(diamond,client,pool)

        print("Clients public key")
        print(client.getPublicKey())


    return (chain, pool)

def login(chain, pool):
    name = input("Enter name: ")
    input("Enter Password: ")

    print("Welcome back")

    return (chain, pool)