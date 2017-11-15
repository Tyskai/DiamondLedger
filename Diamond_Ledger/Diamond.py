# Diamond Class
# unique Id will be generated based on diamond features
# This class only creates a new diamond with given properties
import hashlib
dNumber = 0

def createHash(message=""):
    return hashlib.sha256(str(message).encode('utf-8')).hexdigest()


class Diamond:

# Create a Diamond with a unique id
    def __init__(self, color, clarity, cut, carat, origin, isnatural):

        self.color = color # integer value between 0-7
        self.clarity = clarity # integer value
        self.cut = cut # integer value
        self.carat = carat # double value
        self.origin = origin # string
        self.isNatural = isnatural # boolean

        global dNumber
        dNumber += 1

        message = "{0}{1}{2}{3}{4}{5}{6}".format(str(self.color), str(self.clarity), str(self.cut), str(self.carat),
                                              str(self.origin), str(self.isNatural),str(dNumber))
        self.uID = createHash(message)

# Print Diamond Features
    def printDiamond(self):
        print("ID: {0}\nColor: {1}\nClarity: {2}\nCut: {3}\nCarat: {4}\nOrigin: {5}\nNatural: {6}".format(str(self.uID),
                                            str(self.color), str(self.clarity), str(self.cut), str(self.carat),
                                            str(self.origin), str(self.isNatural)))


#d = Diamond(3,3,4,5,"Indonesia",True)
#d2 = Diamond(3,3,4,5,"Indonesia",True)
#d3 = Diamond(3,3,4,5,"Indonesia",True)

#print(d.printDiamond())
#print(d2.printDiamond())
#print(d3.printDiamond())


