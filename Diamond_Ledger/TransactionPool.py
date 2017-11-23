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

    #remove invalid transactions
    def removeInvalidTransactions(self):
        for t in self.pool:
            if t["Valid"] == False:
                self.pool.remove(t)

    def validateTransaction(self,transaction, state, publicKey):
        indice = [i for i in TransactionPool.getTransactionPool(self) if
                  i["Diamond"] == transaction["Diamond"] and i["Current Owner"] == transaction["Current Owner"] and
                  i["Current Owner"] != i["Next Owner"]]
        if len(indice) > 1:
            print("Cannot transfer same diamond twice!!")
            return False
        if (transaction["Header"] != hashlib.sha256(transaction["Diamond"].getDiamond().encode('utf-8')).hexdigest() + transaction["Current Owner"] + transaction["Next Owner"]):
            print("Header is not valid.")
            return False
        headerHash = hashlib.sha256(transaction["Header"].encode('utf-8')).hexdigest()
        if not Key.verify(headerHash, transaction["Signature"], publicKey):
            print("Signature is not valid!")
            return False
        if not (element for element in state.getState() if
                element["Diamond"] == transaction["Diamond"] and element["Owner"] == transaction["Current Owner"]):
            print("Transaction is not valid")
            return False
        if not (transaction["Diamond"].validateDiamond()):
            print("Diamond ID is not valid. Suspicion: tampered with the diamond values")
            return False
        indice = []
        return True

    # Valide all the transactions
    # Remove all invalid transacionts
    def validateTransactionS(self, state,publicKey):
        for t in self.pool:
            clientPublicKey = [i for i in publicKey if i[0] == t["Current Owner"]]
            t["Valid"] = self.validateTransaction(t,state,clientPublicKey[0][1])

    def diamondExists(self, diamondId):
        for t in self.pool:
            if diamondId == t["Diamond"].getDID():
                return True
        return False

    def getTransactionPool(self):
        return self.pool

    def removeTransactions(self, num = 5):
        del self.pool[0:num]

    def removeLastTransaction(self):
        del self.pool[-1]

    def __len__(self):
        return len(self.pool)

    def printPool(self):
        for i in self.pool:
            print(i)

    def getLastTransaction(self):
        return self.pool[-1]

