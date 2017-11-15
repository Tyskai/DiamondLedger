# Generate private/public key pairs
# Private key is a random long integer -- find a better trustful random number generator
# Public key is the hash of private key
import random ,hashlib

# Find a way to define this function globally
def createHash(message=""):
    return hashlib.sha256(str(message).encode('utf-8')).hexdigest()

# Elliptic curve dsa - the secp256k1
# Recommended 256-bit Elliptic curve Domain Parameters
FiniteP = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F # the prime p that specifies the size of the finite field
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 #The order n of the subgroup
# The coeffivients a and b of the ec equation
a_curve = 0 
B_curve = 7
#The base point G that generates the subgroup
GenX =0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
GenY =0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
GPoint = (GenX,GenY)

class Key:

# Generate key pairs, seed might bee taken from client
    def __init__(self):
        self.privKey = random.randrange(1,N-1)
        print("priveKey: ",self.privKey)
        xPublicKey, yPublicKey = EcPointMultiplication(GenX,GenY,self.privKey)
        finalPublicKey = xPublicKey,yPublicKey
        print("finalpublickey: ", finalPublicKey) 
        self.publicKey = createHash(str(finalPublicKey))

    def getPrivateKey(self):
        return str(self.privKey) # check after changing the rand function

    def getPublicKey(self):
        return self.publicKey
    
#random integer that is needed to sign the message
RandNum = random.randrange(1,N-1)
# the hash of your message/transaction
HashOfThingToSign = 86032112319101611046176971828093669637772856272773459297323797145286374828050

#Returns (gcd,x,y) -> ma+nb=gcd(a,b)
def extended_euclidean_algorithm(a, b):
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t

#multiplicative inverse
def modularinverse(n, p=FiniteP):
    gcd, x, y = extended_euclidean_algorithm(n, p)
    assert (n * x + p * y) % p == gcd

    if gcd != 1:
        # Either n is 0, or p is not a prime number.
        raise ValueError(
            '{} has no multiplicative inverse '
            'modulo {}'.format(n, p))
    else:
        return x % p
#Point addition in elliptic curve
def PointAddition(x_1,y_1,x_2,y_2): 
    lmbda = ((y_2-y_1) * modularinverse(x_2-x_1,FiniteP)) % FiniteP
    x_3 = (lmbda**2-x_1-x_2) % FiniteP
    y_3 = (lmbda*(x_1-x_3)-y_1) % FiniteP
    return (x_3,y_3)

#Point addition for when 2 points are the same
def PointDoubling(x_1,y_1): 
    dblmbda = ((3*x_1**2+a_curve) * modularinverse((2*y_1),FiniteP)) % FiniteP
    x_3 = (dblmbda**2-2*x_1) % FiniteP
    y_3 = (dblmbda*(x_1-x_3)-y_1) % FiniteP
    return (x_3,y_3)

#Not an actual multiplication just point doubling and adding
def EcPointMultiplication(xs,ys,Scalar):
    if Scalar == 0 or Scalar >= N:
        raise Exception("Invalid Scalar/Private Key")
    ScalarBin = str(bin(Scalar))[2:]
    Qx,Qy=xs,ys
    for i in range (1, len(ScalarBin)): 
        Qx,Qy=PointDoubling(Qx,Qy);
        if ScalarBin[i] == "1":
            Qx,Qy=PointAddition(Qx,Qy,xs,ys);
    return (Qx,Qy)

"""
print("******* Public Key Generation *********")
xPublicKey, yPublicKey = EcPointMultiplication(GenX,GenY,self.privKey)
print("the private key (in base 10 format):")
print("privekey: ",self.privKey,"\n")
print("the uncompressed public key (starts with '04' & is not the public address):") 
print("04",xPublicKey,yPublicKey,"\n")
finalPublicKey = xPublicKey,yPublicKey
print("finalpublickey: ",finalPublicKey)

print("******* Signature Generation *********")
xRandSignPoint, yRandSignPoint = EcPointMultiplication(GenX,GenY,RandNum)
r = xRandSignPoint % N
print("r =", r)
s = ((HashOfThingToSign + r*privKey)*(modularinverse(RandNum,N))) % N
print("s =", s)

print("******* Signature Verification *********>>")
w = modularinverse(s,N)
xu1, yu1 = EcPointMultiplication(GenX,GenY,(HashOfThingToSign * w)%N)
xu2, yu2 = EcPointMultiplication(xPublicKey,yPublicKey,(r*w)%N)
x,y = PointAddition(xu1,yu1,xu2,yu2)
print(r==x)
"""

k = Key()
print(k.getPublicKey(),"\n", k.getPrivateKey())
