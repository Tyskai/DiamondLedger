# State class
# Keeps track of applied transactions and updates the state
from Diamond_Ledger import Transaction
class State:

    def __init__(self):
        self.state = list() # will be a list of all ownerships

    def updateState(self,transactions, num = 5):
        t = [j for j in transactions.getTransactionPool() if j["Valid"] == True]
        for i in range(num):

            currentOwner = t[i]["Current Owner"]
            diamond = t[i]["Diamond"]
            nextOwner = t[i]["Next Owner"]

            currentOwnership = {"Diamond":diamond,"Owner":currentOwner}
            nextOwnership = {"Diamond":diamond,"Owner":nextOwner}

            self.state.append(nextOwnership)
            if not (nextOwner == currentOwner):
                self.state.remove(currentOwnership)


    def getState(self):
        return self.state

    def emptyState(self):
        del self.state[len(self.state)]

    def __len__(self):
        return len(self.state)

    def initializeState(self, ownership):
        self.state = ownership

        # Print block info
    def printState(self):
        print("Ownership of current state")
        for i in range(len(self.state)):
            print("Number : {0}{1}".format(i, self.state[i]))
        print("\n")