# Diamond Class
# unique Id will be generated based on diamond features
# This class only creates a new diamond with given properties
import hashlib
dNumber = 0

def createHash(message):
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

        message = "{0}{1}{2}{3}".format(str(self.color), str(self.clarity), str(self.cut), str(self.carat))
        self.uID = createHash(message)

# Print Diamond Features
    def printDiamond(self):
        print("ID: {0}\n    Color: {1}\n    Clarity: {2}\n    Cut: {3}\n    Carat: {4}\n    Origin: {5}\n    "
                                            "Natural: {6}\n".format(str(self.uID),
                                            str(self.color), str(self.clarity), str(self.cut), str(self.carat),
                                            str(self.origin), str(self.isNatural)))
    def diamondString(self):
        return "ID: {0}\nColor: {1} Clarity: {2} Cut: {3} Carat: {4} Origin: {5} Natural: {6}".format(str(self.uID),
                                            str(self.color), str(self.clarity), str(self.cut), str(self.carat),
                                            str(self.origin), str(self.isNatural))

    def getDiamond(self):
        return "{0}{1}{2}{3}{4}{5}{6}".format(str(self.uID), str(self.color), str(self.clarity), str(self.cut),
                                          str(self.carat), str(self.origin), str(self.isNatural))

    def getDID(self):
        return self.uID

    def setDID(self, newID):
        self.uID = newID

    def validateDiamond(self):
        message = "{0}{1}{2}{3}".format(str(self.color), str(self.clarity), str(self.cut), str(self.carat))
        checkID = createHash(message)
        return (self.uID == checkID)

