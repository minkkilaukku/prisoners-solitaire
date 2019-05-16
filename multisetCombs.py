import itertools


#counts how many k-combinations the multiset {nj*j, j=0..r} has,
#where nj's are given by msetCounts
#optional list mustHaves of elements that are required to be present
def bruteCombs(msetCounts, k, mustHaves=[]):
    M = []
    for j in xrange(len(msetCounts)):
        M += [j]*msetCounts[j]

    needToCheckMustHaves = len(mustHaves)>0
    def checkMustHaves(comb):
        for h in mustHaves:
            if h not in comb: return False
        return True

    A = set() #store all combs here as tuples (ignores duplicates)
    
    for comb in itertools.combinations(M, k):
        if (not needToCheckMustHaves) or checkMustHaves(comb):
            A.add(tuple(sorted(comb)))
            
    return A


njs = [1,4,4]
k = 3
mustHaves = range(1)
a = bruteCombs(njs, k)
b = bruteCombs(njs, k, mustHaves)
print "multisets %i-combinations with nj's = %s" %(k, str(njs))
print "with must have "+str(mustHaves)+":"
print len(b)
print "all:"
print len(a)
