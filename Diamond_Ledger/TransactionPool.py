# TransactionPool class
# Collect all transactions and validate them
# After validation Transaction pool updates transaction state -- sends invocation to client
from Diamond_Ledger import Transaction


class TransactionPool:

    def __init__(self):
        self.pool = list() # will be a list of directories

    def addTransaction(self,transaction):
        # first validate transaction then add
        TransactionPool.validateTransaction(self,transaction)
        self.pool.append(transaction)

    def validateTransaction(self,transaction):
            transaction["Valid"] = True
            #print("Transaction is validated")
            pass
            # check if there is an empty element in the directory
            # if there is then return false with a error message
            #if all the features are proper change transaction state to true
            # update it alson on client side
            # transaction["Valid"]=return validateTransaction

    def getTransactionPool(self):
        return self.pool

    def removeTransactions(self):
        del self.pool[0:5]

    def __len__(self):
        return len(self.pool)