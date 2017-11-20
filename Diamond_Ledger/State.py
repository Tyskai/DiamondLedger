# State class
# Keeps track of applied transactions and updates the state
from Diamond_Ledger import Transaction
class State:

    def __init__(self):
        self.state = list() # will be a list of all ownerships

    def updateState(self,transactions):
        for i in range(5):
            t = transactions.getTransactionPool()[i]
            currentOwner = t["Current Owner"]
            diamond = t["Diamond"]
            nextOwner = t["Next Owner"]

            currentOwnership = {"Diamond":diamond,"Owner":currentOwner}
            nextOwnership = {"Diamond":diamond,"Owner":nextOwner}

            self.state.append(nextOwnership)
            try:
                self.state.remove(currentOwnership)
                break
            except ValueError:
                a = "A new diamond is added to the system"
                #print(a)

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