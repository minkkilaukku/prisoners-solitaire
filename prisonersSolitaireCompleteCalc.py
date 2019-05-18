import itertools, fractions
from collections import Counter

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


#ps = list of lists with non-negative entries sorted in ascending order
#r = the wanted sum for an element of p1 x p2 x...x pm
def productThatSumTo(ps, r, currSum=0):
    if len(ps)==0:
        if currSum==r: return [[]]
        else: return []
    
    ret = []
    others = ps[1:]
    for x in ps[0]:
        if currSum+x > r: break #since all non-neg ascending, can't find anymore
        ret += [ [x] + a for a in productThatSumTo(others, r, currSum+x)]
    return ret


def generMulticombs(elems, k):
    counts = Counter(elems)
    for sub_counts in productThatSumTo([range(n+1) for n in counts.values()], k):
        yield list(Counter(dict(zip(counts.keys(), sub_counts))).elements())


def nextMultipermu(a):
    n = len(a)
    m = 0
    #Find the next different value
    for i in xrange(1, n):
        if (a[i-1] < a[i]):
            m = i

    if (m == 0): return a, False

    #sort a[m+1:n]
    if (m+1 < n):
        for i in xrange (m, n):
            for j in xrange (i+1, n):
                if (a[j] < a[i]):
                    t = a[i]
                    a[i] = a[j]
                    a[j] = t
    
    i = 1
    while (a[m+i-1] <= a[m-1]): i = i+1

    temp = a[m-1]
    a[m-1] = a[m+i-1]
    a[m+i-1] = temp

    return a, True

#Generate all permutations of the array, ignoring duplicates
#(two permutations are duplicates if they have the same elements in same order)
def generCompleteMultipermus(arr):
    a = sorted(arr[:])
    yield a[:]
    hasNext = True
    while hasNext:
        p, hasNext = nextMultipermu(a)
        if not hasNext: break
        yield p[:]

#Generate k-multipermus or the array arr
def generMultipermus(arr, k):
    for c in generMulticombs(arr, k):
        for p in generCompleteMultipermus(c):
            yield p



def getFactFact(multipermu, suits):
    counts = Counter(multipermu)
    ret = 1
    for x in counts.values():
        ret *= factorial(x)*binCoeff(suits, x)
    return ret



def calcProbBrute(suits, vals, boardN, pickN):
    deck = []
    for i in xrange(vals):
        deck += [i]*suits

    def isGood(b, h):
        for x in b:
            if x not in h: return False
        return True
    
    tot = 0
    good = 0
    for perm in itertools.permutations(deck, boardN+pickN):
        if (isGood(perm[:boardN], perm[boardN:])):
            good += 1
        tot += 1
    return fractions.Fraction(good, tot)



def calcProbBrute2(suits, vals, boardN, pickN):
    deck = []
    for i in xrange(vals):
        deck += [i]*suits

    def isGood(b, h):
        for x in b:
            if x not in h: return False
        return True
    
    tot = 0
    good = 0
    permSize = boardN+pickN
    a = []
    goodA = []
    for perm in generMultipermus(deck, permSize):
        #how many times this appears in normal permus
        w = getFactFact(perm, suits)
        a.append(perm)
        if (isGood(perm[:boardN], perm[boardN:])):
            goodA.append(perm)
            good += w
        tot += w
    #print "all:"
    #print a
    #print "good:"
    #print goodA
    return fractions.Fraction(good, tot)



suits = 4
vals = 3
boardN = vals
pickN = boardN

p = calcProbBrute(suits, vals, boardN, pickN)
print "{} = {}".format(str(p), str(float(p)))

print "multipermu way:"
p = calcProbBrute2(suits, vals, boardN, pickN)
print "{} = {}".format(str(p), str(float(p)))




##deck = range(2)*3
##a = list(generMultipermus(deck, 3))
##b = list(itertools.permutations(deck, 3))
##print len(a)
##print len(b)
##print "weightted sum of a:"
##print sum([ getFactFact(x, 3) for x in a ])

