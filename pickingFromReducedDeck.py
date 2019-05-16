import itertools


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

def getAllPossibleTypes(boardN, suits, vals):
    return getPartitions(boardN, min(boardN, vals), suits)



def bruteThePick(t, pickN, suits, vals):
    deck = [x%vals for x in xrange(suits*vals)]
    tLen = len(t)
    #we can assume the removed ones are in order (remove t[i] i's)
    for i in xrange(tLen):
        for j in xrange(t[i]):
            deck.remove(i)
    ret = 0
    a = []
    def hasAtLeastOneOfEach(hand):
        for i in xrange(tLen):
            if i not in hand: return False
        return True
    
    for comb in itertools.combinations(deck, pickN):
        hand = [x%vals for x in comb]
        if hasAtLeastOneOfEach(hand):
            ret+=1
            a.append(hand)
    #print a
    return ret


#given the board type t, get a list of all deck picking types that will
#clear it and are possible
#deck picking type is a vector (a1, a2,..., ar) telling how many to
#pick of each number in the type t (notice: these can be assumed to be
#the numbers 0..r
def getGoodTypes(t, suits, vals, pickN):
    maxes = [suits-x for x in t]
    ret = []

    def isGood(p):
        if len(p)<len(t): return False
        for i,x in enumerate(p):
            if x==0 or x>maxes[i]: return False
        return True
    for p in itertools.product( *[range(1, m+1) for m in maxes] ):
        if isGood(p): ret.append(p)
    return ret

#if deck has multiplicities njs
#how many pickN-combinations has the given type t
def bruteThePickOfType(njs, t, pickN, suits, vals):
    print "bruting of type {}".format(str(t))
    deck = []
    for j in xrange(len(njs)):
        deck += [j]*njs[j]
    tLen = len(t)
    ret = 0
    a = []
    #how many of each value in hand, last is the others
    def getCounts(hand):
        ret = [0]*(tLen+1)
        for x in hand: ret[min(x, tLen)]+=1
        return ret
    
    def isCorrectType(hand):
        counts = getCounts(hand)
        c = "hello"
        for i in xrange(tLen):
            if counts[i]!=t[i]: return False
        return True
    
    for hand in itertools.combinations(deck, pickN):
        if isCorrectType(hand):
            a.append(hand)
            ret+=1
    #print a
    return ret


def calcPickOfType(njs, t, pickN, suits, vals):
    restN = sum(njs[len(t):])
    restA = pickN-sum(t)

    ret = binCoeff(restN, restA)
    for i in xrange(len(t)):
        ret *= binCoeff(njs[i], t[i])
    return ret


def calcBStuff(t, pickN, suits, vals):
    goodDeckTypes = getGoodTypes(t, suits, vals, pickN)
    njs = [suits-x for x in t] + [suits]*(vals-len(t))
    ret = 0
    for t2 in goodDeckTypes:
        ret += calcPickOfType(njs, t2, pickN, suits, vals)
    return ret

    

suits = 4
vals = 5
boardN = 3
pickN = 3

n = suits*vals
t = [3, 2]
njs = [suits-x for x in t] + [suits]*(vals-len(t))

print "all"
print bruteThePick(t, pickN, suits, vals)

print calcBStuff(t, pickN, suits, vals)


##for t2 in [ [1,1], [1,2], [2,1] ]:
##    print "type "+str(t2)
##    print bruteThePickOfType(njs, t2, pickN, suits, vals)
##    print calcPickOfType(njs, t2, pickN, suits, vals)
##    

#print bruteThePickOfType(njs, [1, 2], pickN, suits, vals)








                         
