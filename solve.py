#A python script for computing stats related to the classic "shut the box" game


import random
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


print(findStats(maxTheMax))




