# TransactionPool class
# Collect all transactions and validate them
# After validation Transaction pool updates transaction state -- sends invocation to client
from Diamond_Ledger.Key import Key
import hashlib

def search_dictionaries(key, value, list_of_dictionaries):
    return [element for element in list_of_dictionaries if element[key] == value]

class TransactionPool:

    def __init__(self):
        self.pool = list() # will be a list of directories

    def addTransaction(self,transaction):
        # first validate transaction then add
        self.pool.append(transaction)

    def validateTransaction(self,transaction,state,publicKey=""):
        if publicKey != "":
            headerHash = hashlib.sha256(transaction["Header"].encode('utf-8')).hexdigest()
            if not Key.verify(headerHash,transaction["Signature"],publicKey):
                print("Signature is not valid!")
                return False
        if not (element for element in state.getState() if element["Diamond"] == transaction["Diamond"] and element["Owner"] == transaction["Current Owner"]):
            print("Transaction is not valid")
            return False
        if not( transaction["Diamond"].validateDiamond() ):
            print("Diamond ID is not valid. Suspicion: tamperd with the diamond values")
        return True

    # Valide all the transactions
    def validateTransactionS(self, state):
        for t in self.pool:
            if t["Valid"] == False:
                t["Valid"] = self.validateTransaction(t,state)

    def getTransactionPool(self):
        return self.pool

    def removeTransactions(self, num = 5):
        del self.pool[0:num]

    def __len__(self):
        return len(self.pool)

    def printPool(self):
        for i in self.pool:
            print(i)