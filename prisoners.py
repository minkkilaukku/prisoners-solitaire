import random, itertools, time
from fractions import Fraction


binoMemo = {}
def binCoeff(n, k):
    global binoMemo
    if (n, k) in binoMemo: return binoMemo[(n,k)]
    if k < 0 or k > n: return 0
    if k == 0 or k == n: return 1
    ret = 1
    for i in range(min(k, n-k)):
        ret = ret*(n-i)//(i+1)
    binoMemo[(n,k)] = ret
    return ret

def factorial(n):
    ret = 1
    for i in xrange(1, n+1): ret *= i
    return ret


def simulate(suits, vals, toTable, pickN, simuN):
    n = suits*vals
    deck = range(vals)*suits
    counts = [0]*(toTable+1)
    for simuI in xrange(simuN):
        random.shuffle(deck)
        table = deck[:toTable]
        for i in xrange(toTable, toTable+pickN, 1):
            checkCard = deck[i]
            while (checkCard in table): table.remove(checkCard)
        counts[len(table)] += 1
    return [ float(c)/simuN for c in counts ]


#a = simulate(4, 13, 13, 13, 1000000)
#print a

"""

[0.003684, 0.019757, 0.057399, 0.112326, 0.166822, 0.192893, 0.178376, 0.13297, 0.080209, 0.037674, 0.013611, 0.003602, 0.000631, 4.6e-05]

"""


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


#list of the pile sizes of the hand when same-valued are piled
#and the piles sorted (larger ones first)
def getType(hand):
    t = {}
    for c in hand:
        if c not in t: t[c] = 0
        t[c] += 1
    return sorted(t.values(), reverse=True)

def countTypes(suits, vals, handLen):
    ret = {}
    n = suits*vals
    for comb in itertools.combinations(xrange(n), handLen):
        hand = [x%vals for x in comb]
        t = tuple(getType(hand))
        if t not in ret: ret[t] = 0
        ret[t] += 1
    return ret

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



def bruteThePick(t, pickN, suits, vals):
    deck = [x%vals for x in xrange(suits*vals)]
    tLen = len(t)
    #we can assume the removed ones are in order (remove t[i] i's)
    for i in xrange(tLen):
        for j in xrange(t[i]):
            deck.remove(i)
    ret = 0
    
    def hasAtLeastOneOfEach(hand):
        for i in xrange(tLen):
            if i not in hand: return False
        return True
    
    for comb in itertools.combinations(deck, pickN):
        hand = [x%vals for x in comb]
        if hasAtLeastOneOfEach(hand): ret+=1

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

def calcPickOfType(njs, t, pickN, suits, vals):
    restN = sum(njs[len(t):])
    restA = pickN-sum(t)

    ret = binCoeff(restN, restA)
    for i in xrange(len(t)):
        ret *= binCoeff(njs[i], t[i])
    return ret



#When cards are removed from the deck so that they form the pile type t,
#in how many ways can pickN cards be picked from the remaining deck
#so that the pick includes at least 1 of each value that is present in removed
#ones
#The original deck is {suits}x{vals}
def calcPickHasAtLeastOneOccurs(t, pickN, suits, vals):
    goodDeckTypes = getGoodTypes(t, suits, vals, pickN)
    njs = [suits-x for x in t] + [suits]*(vals-len(t))
    ret = 0
    for t2 in goodDeckTypes:
        ret += calcPickOfType(njs, t2, pickN, suits, vals)
    return ret







#TODO still with second part brute
#Calculate the probability of winning prisoner's solitaire
#deck = {suits}x{vals}
#handLen: how many cards are placed on board in phase 1
#pickN: how many cards picked from the remaining deck in phase 2
def calculateProb(suits, vals, handLen, pickN):
    ts = getPartitions(handLen, min(handLen, vals), suits)
    n = suits*vals
    b1 = binCoeff(n, handLen)
    b2 = binCoeff(n-handLen, pickN)
    bTot = b1*b2

    aTot = 0
    for t in ts:
        a1 = calcTypeOccurs(t, suits, vals)
        a2 = calcPickHasAtLeastOneOccurs(t, pickN, suits, vals)
        aTot += a1*a2

    return Fraction(aTot, bTot)


suits = 4
vals = 13 #13 takes quite long
boardN = vals
pickN = vals

startTime = time.time()
p = calculateProb(suits, vals, boardN, pickN)
tookTime = time.time()-startTime
print "took "+str(tookTime)

print "{} = {}".format(str(p), float(p))

print "simu"
simuP = simulate(suits, vals, boardN, pickN, 40000)
print simuP[0]

####### The Result #####################################
#
#   calculateProb(4, 13, 13, 13) =
#   964444044208/262190765217675 = 0.00367840584853
#
########################################################
# without memorizing binocoeffs: took 110.651000023
# with memo: took 72.236000061


