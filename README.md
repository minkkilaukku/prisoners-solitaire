# prisoners-solitaire
All sorts of simulations and calculations of the card game called Prisoner's Solitaire

Try it out at https://prisoners-solitaire--minkkilaukku2.repl.co/


**Edit**

Now it gives the winning probability for 4*13 cards: 964444044208/262190765217675 = 0.00367840584853. But it takes a couple of minutes. The second (clearing) probabilities are calculated like this: for a type t, consider all the allowed and >=1 pickings from the deck for the numbers 0..|t|, for that ways of picking is a product of binomial coefficients. Add those up to get the wanted ways of picking.



**Old way ponderings**


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



#EDIT
Well, of course, different combinations of the multiset have different probability to come! Now, how to include these probabilities in the formula. Maybe we should consider the permutations (and use EGF's)?

For example all combs resulting from the type t = [3] are

[[1, 2, 0], [1, 1, 0], [1, 2, 0], [1, 1, 0], [1, 2, 0], [1, 0, 1], [1, 0, 2], [2, 1, 0], [2, 2, 0], [2, 1, 0], [2, 2, 0], [2, 0, 1], [2, 0, 2], [1, 2, 0], [1, 1, 0], [1, 2, 0], [1, 0, 1], [1, 0, 2], [2, 1, 0], [2, 2, 0], [2, 0, 1], [2, 0, 2], [1, 2, 0], [1, 0, 1], [1, 0, 2], [2, 0, 1], [2, 0, 2], [0, 1, 2]]

but when regarded as aifaäld'ada there are only 3 different ones:

['0,1,1', '0,1,2', '0,2,2']




