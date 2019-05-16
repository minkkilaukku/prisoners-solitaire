# prisoners-solitaire
All sorts of simulations and calculations of the card game called Prisoners Solitaire

Try it out at https://prisoners-solitaire--minkkilaukku2.repl.co/

The "combinations of multiset" -way doesn't work.
For example for parameters
    suits = 4
    vals = 3
    boardN = 3
    pickN = 3

**explanation:**
aProbs are the probabilities for getting a particular type on the board (partitions of boardN to parts <= suits).
bProbs are probabilities of clearing the board when it has a particular type (the deck has that type subtracted from it).

we have for the types
    ts = [ [3], [2,1 , [1,1,1] ]
    aProbs = [3/55, 36/55, 16/55]
and we get wrong
    bProbs = [ 3/7, 1/3, 1/10 ]
they should be
    [ 1/3, 11/28, 9/28 ]
which have been calculated by brute force and give the correct winning probability 142/385, which is also checked by brute force.
