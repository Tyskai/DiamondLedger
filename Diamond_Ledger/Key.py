# Generate private/public key pairs
# Private key is a random long integer -- find a better trustful random number generator
# Public key is the hash of private key
import random ,hashlib

# Find a way to define this function globally
def createHash(message=""):
    return hashlib.sha256(str(message).encode('utf-8')).hexdigest()

class Key:

# Generate key pairs, seed might bee taken from client
    def __init__(self):
        self.privateKey = random.getrandbits(32) # find a secure function
        self.publicKey = createHash(str(self.privateKey))

    def getPrivateKey(self):
        return str(self.privateKey) # check after changing the rand function

    def getPublicKey(self):
        return self.publicKey


#k = Key()
#print(k.getPublicKey()+"\n"+ str(k.getPrivateKey()))