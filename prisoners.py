import random, itertools, fractions


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


#When cards are removed from the deck so that they form the pile type t,
#in how many ways can pickN cards be picked from the remaining deck
#so that the pick includes at least 1 of each value that is present in removed
#ones
#The original deck is {suits}x{vals}
def calcPickHasAtLeastOneOccurs(t, pickN, suits, vals):
    return 1 #TODO




#39 possible types
#print getPartitions(13, 13, 4)


#testing type occurance calculation
##suits = 3
##vals = 5
##handLen = 5
##a = countTypes(suits, vals, handLen)
##print "suits  = %i, vals = %i, handLen = %i" %(suits, vals, handLen)
##print "How the combinations distribute among types"
##print "type \t brute \t calculated"
##for k in sorted(a.keys(), reverse=True):
##    print str(k) + "\t" + str(a[k]) + "\t" + str(calcTypeOccurs(k, suits, vals))



#testing picking from the remains occurance calculation
suits = 3
vals = 5
handLen = 5
pickN = 5
ps = getPartitions(handLen, handLen, suits)
brutes = [bruteThePick(t, pickN, suits, vals) for t in ps]
calcs = [calcPickHasAtLeastOneOccurs(t, pickN, suits, vals) for t in ps]
print ("suits  = %i, vals = %i, handLen = %i, pickN = %i"
       %(suits, vals, handLen, pickN) )
print "How many ways to pick the remaining such that have at least 1 of each"
print "type \t brute \t calculated"
for i in xrange(len(ps)):
    print ( str(ps[i]) +
           "\t" + str(brutes[i]) +
           "\t" + str(calcs[i]) )


























