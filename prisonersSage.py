import fractions

R.<z> = QQ['z']

def binCoeff(n, k):
    if k < 0 or k > n: return 0
    if k == 0 or k == n: return 1
    ret = 1
    for i in range(min(k, n-k)):
        ret = ret*(n-i)//(i+1)
    return ret

def factorial(n):
    ret = 1
    for i in xrange(1, n+1): ret *= i
    return ret

#list of partitions of n to at most maxPartsN parts that are at most maxSize
def getPartitions(n, maxPartsN, maxSize):
    if n==0: return [[]]
    canMakeMax = maxPartsN*maxSize
    if n>canMakeMax: return []
    if n==canMakeMax: return [[maxSize]*maxPartsN]
    ret = []
    for x in xrange(min(n, maxSize), -1, -1):
        ret += [[x] + sP for sP in getPartitions(n-x, maxPartsN-1, x)]
    return ret

def getAllTypes(suits, vals, boardN, pickN):
    return getPartitions(boardN, min(boardN, vals), suits)

def typeToRemainingDeckNjs(t, suits, vals):
    return [suits- (t[i] if i<len(t) else 0) for i in range(vals)]



def countMultiCombs(njs, k, mustHave=[]):
    g = 1 #the generating polynomial for suotuisat
    gAll = 1 #for all
    #it is the product
    for i in range(len(njs)):
        giCoeffs = [1]*(njs[i]+1)
        if i in mustHave:
            giCoeffs[0] = 0
        g *= R(giCoeffs)
        
    return g[k]


def getTypeInnerPermuFactor(t):
    counts = {}
    for x in t:
        if x not in counts: counts[x] = 0
        counts[x] += 1
    ret = 1
    for x in counts: ret *= factorial(counts[x])
    return ret


#in how many ways can the type t come from the deck {suits}x{vals}
#(hand length is sum(t))
def calcTypeOccurs(t, suits, vals):
    ret = 1
    bCoeffs = [binCoeff(suits, x) for x in xrange(suits+1)]
    for i in xrange(len(t)):
        ret *= (vals-i)*bCoeffs[t[i]]
    return ret/getTypeInnerPermuFactor(t)


#probability of getting a type t when drawing from deck {1..suits}x{1..vals}
def probOfTypeToBoard(t, suits, vals):
    numer = calcTypeOccurs(t, suits, vals)
    denom = binCoeff(suits*vals, sum(t))
    return fractions.Fraction(int(numer), int(denom)) #they are Sage integers, convert to Python

#probability for clearing all the cards on table when the ones on board form a type t, and pickN cards are picked from the remaining deck
def probOfClearFromDeck(t, suits, vals, pickN):
    njs = typeToRemainingDeckNjs(t, suits, vals)
    numer = countMultiCombs(njs, pickN, range(len(t)))
    denom = countMultiCombs(njs, pickN)
    return fractions.Fraction(int(numer), int(denom))


def calcWinProb(suits, vals, boardN, pickN):
    ts = getAllTypes(suits, vals, boardN, pickN)
    aProbs = [probOfTypeToBoard(t, suits, vals) for t in ts]
    bProbs = [probOfClearFromDeck(t, suits, vals, pickN) for t in ts]
    print aProbs
    print bProbs
    return sum([aProbs[i]*bProbs[i] for i in range(len(ts))])


p = calcWinProb(4, 13, 13, 13)
print str(p) + " = "+str(float(p))
#0.00122300032504, doesn't seem right, should be 0.0037, hmm....


#p = probOfTypeToBoard([3, 2, 2, 2, 1, 1, 1, 1], 4, 13)
#print str(p) + " = "+str(float(p))

##vals = 5 #13
##k = 7 #13
##t = [3,2,1] #[3, 2, 2, 2, 1, 1, 1, 1]
###njs = [4- (t[i] if i<len(t) else 0) for i in range(vals)]

##print countMultiCombs(njs, k, range(len(t)))
##print countMultiCombs(njs, k)