import itertools, fractions


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
        if (isGood(perm[:boardN], perm[boardN:])): good += 1
        tot += 1

    return fractions.Fraction(good, tot)


p = calcProbBrute(4,3,2,2)
print "{} = {}".format(str(p), str(float(p)))
