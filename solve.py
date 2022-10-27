#A python script for computing stats related to the classic "shut the box" game


import random
import copy
import sys
sys.setrecursionlimit(10000)


NUM_TRIALS = 10000

#game strategy
def maxTheMax(dieRoll, dominos):
    if dieRoll < 0:
        return False
    elif dieRoll == 0:
        return True
    for valueToAchieve in range(min(dieRoll, 10), 0, -1):
        idx = valueToAchieve - 1
        if dominos[idx]:
            dominos[idx] = False
            if maxTheMax(dieRoll - valueToAchieve, dominos):
                return True
            else:
                dominos[idx] = True

    return False


def minCost(costs):

    #subset is a decimal number encoding binary string telling us which dominos to pick
    #0 <= n < len(dominos)
    #the rightmost portion of the string corresponds to lower value dominos
    def extractBit(subset, n):
        return (subset >> n) % 2

    def iterateSubsetSums(L, k):
        for subset in range(2**(len(L))):
            v = 0
            total = 0
            for dominoValue in range(1, len(L) + 1):
                if L[dominoValue - 1] and extractBit(subset, dominoValue - 1):
                    total += dominoValue
            if total == k:
                yield subset

    def subsetCost(subset, dominos):
        cost = 0
        for i in range(len(dominos)):
            cost += costs[i]*(extractBit(subset, i))
        return cost

    def strategy(dieRoll, dominos):

        bestCost = None
        bestSubset = None
        for subset in iterateSubsetSums(dominos, dieRoll):
            thisCost = subsetCost(subset, dominos)
            if bestCost == None or thisCost < bestCost:
                bestSubset = subset
                bestCost = thisCost


        if bestCost != None:
            for i in range(len(dominos)):
                if extractBit(bestSubset, i):
                    dominos[i] = False
            return True


        return False


    return strategy

basicCost = minCost([100, 8, 6, 4, 2, 0, -2, -4, -60, -800])

def sumDominos(dominos):
    score = 0
    for i in range(len(dominos)):
        if dominos[i]:
            score += (i + 1)
    return score



def runGame(strategy):
    #true is up and false is down
    dominos = [True] * 10
    dieRoll = random.randint(1, 6) + random.randint(1, 6)
    while strategy(dieRoll, dominos):
        if sumDominos(dominos) <= 6:
            dieRoll = random.randint(1, 6)
        else:
            dieRoll = random.randint(1, 6) + random.randint(1, 6)
    return sumDominos(dominos)



def findStats(strategy):
    runningAverage = 0
    numTimesShut = 0
    for i in range(NUM_TRIALS):
        result = runGame(strategy)
        runningAverage += result
        if result == 0:
            numTimesShut += 1
    probabilityofShutting = numTimesShut/NUM_TRIALS

    return (runningAverage/NUM_TRIALS, probabilityofShutting)

print(findStats(basicCost))



