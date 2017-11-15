# Transaction class
# Contains 2 type of transactions
# createTransaction() -> changes owner ship
# queryDiamond() -> track a diamond on ledger ( for tracking ownership or validation)
from Diamond_Ledger import TransactionPool
from Diamond_Ledger import Diamond

class Transaction:

    #def __init__(self):
    #    self.isValid = False # at first creation transaction is not valid, later it will be validated

# Change diamonds ownership -- later decide if pass diamond itself or its id
    def createTransaction(self,diamond, currentOwner, nextOwner,pool): # returns a directory
        self.transaction = {"Diamond":diamond,"Current Owner":currentOwner,"Next Owner":nextOwner,"Valid":False}
        pool.addTransaction(self.transaction)

# Query a diamond
    def queryDiamond(self,dID):
        pass



#pool = TransactionPool()
#t = Transaction()
#d = Diamond(2,2,3,4,"Alasca",True)
#t.createTransaction(d,234567654,23456543,pool)
#print(pool.getTransactionPool())
