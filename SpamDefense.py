'''
Created on Mar 13, 2015

@author: Jinxue Zhang

Simulate the spam defense by assigning each user a spam score
'''

'''
We first build a network with all the socialbots completely connected 
and each socialbot being followed by certein number of normal users
n: the number of sociabots
f: the number of total followers
mu & sigma: the average and variance of followers for each socialbot
rtRatio: the probability that a legitimate user will retweet a spam

We don't need to build the real network because only the followers of
each socialbot matter. Therefore we just use a dictionary to store the
followers of each socialbot.

We also need to set up a table to store the spam score for each socialbot
and legitimate follower
'''
import random

def networkBuild(n, f, mu, sigma, rtRatio):
#def networkBuild(n, f, mu, sigma):
    expNetwork = dict()
    spamScore = dict()
    
    followerList = range(n + 1, n + f + 1)
    
    # We then build a list containing the legitimate users that will rewteet the spam
    '''
    By setting like this, we obtained a weird result regarding the false positive. All the chosen legitimate
    retweeters will be suspended according to the gamma eventually. Specifically, when the gamma is >= 0.6, all the
    socialbots will be suspended after 7 rounds. Thus all the chosen legitimate users who follow these socialbots
    will be suspended after 8 rounds. This is wrong.
    
    We should randomly select the legitimate retweeters for each round.
    '''
    #retweetUsers = random.sample(followerList, int(f * rtRatio))
    
    for bot in range(1, n + 1):
        num = int(random.gauss(mu, sigma))
        followers = random.sample(followerList, num)
        expNetwork[bot] = followers
        
    for user in range(1, n + 1):
        spamScore[user] = 0
    
    #for user in retweetUsers:
    #    spamScore[user] = 0
    
    return expNetwork, spamScore
'''
As stated before, we should randomly select the legitimate retweeters for each round.

Late Remark::
However, this attack model is also wrong because at each round, r ratio of users will retweet the tweets.
After 10 rounds for r=0.1, all the users will expected to retweet a malicious tweet. 
Hence this attack model is too strong.

The right attack model should be like this:
only r portion of the legitimate users could retweet the spam only once in the whole experiment (composed of 10 rounds)

***************
The bug is like this: once the legitimate retweeter has been chosen at this round, he will retweet the spam in 
all the following rounds.
Thus we just need to make the decision as follows:
1. if the legitimate retweeter has spam score more than 1.0, we will remove it
2. if the legitimate retweeter has been chosen again in this round, we will keep its spam score
3. Otherwise, remove it from the spamScore


*****************
Still have the bug:
the legitimate retweeter who has not been chosen in this round might be chosen in the future, thus we should not
remove them directly

*********
The reason why the FP curves are straight after several rounds is that all the socialbots have been suspended and 
no more legitimate retweeters will be suspended then

Yes, the attack model is still too strong, hence, we need to assume that the retweeting ratio is the one in the
whole experiment. Therefore, in each round, we split them probability to r/10

*** Final issue, we should not let the legitimate retweeter retweet multiple times in a single round because he 
might follow multiple bots. 
By considering this point, we have no need to split the probabilty by the experimental rounds.
'''
def chooseLegRetweeters(n, f, rtRatio, spamScore):
    followerList = range(n + 1, n + f + 1)
    retweetUsers = random.sample(followerList, int(f * rtRatio))
    
    '''
    #tempList = []
    #for user in spamScore:
    #    if user > n:
    #        tempList.append(user)
    #for user in tempList:
    for user in spamScore.keys():
        if user > n and (spamScore[user] >= 1.0 or user not in retweetUsers):
            spamScore.pop(user)
            
    '''
    for user in retweetUsers:
        if user not in spamScore:
            spamScore[user] = 0

    return retweetUsers

'''
Greedy algorithm for NP-hard Minimum cover problem
x: the number of chosen elements
wholeSet: the whole set to choose; it is a dictionary in this project
'''
def minCover(x, wholeSet):
    chosenSet = dict()
    if len(wholeSet) == 0:
        return chosenSet
    if x >= len(wholeSet):
        for user in wholeSet:
            chosenSet[user] = wholeSet[user]
        wholeSet.clear()
        return chosenSet
    for _ in range(0, x):
        gain = 1000000
        for user in wholeSet:
            if len(wholeSet[user]) < gain:
                gain = len(wholeSet[user])
                chosenUser = user
        chosenSet[chosenUser] = wholeSet.pop(chosenUser)
    return chosenSet

def maxCover(x, wholeSet):
    chosenSet = dict()
    if len(wholeSet) == 0:
        return chosenSet
    if x >= len(wholeSet):
        for user in wholeSet:
            chosenSet[user] = wholeSet[user]
        wholeSet.clear()
        return chosenSet
    for _ in range(0, x):
        gain = -1
        for user in wholeSet:
            if len(wholeSet[user]) > gain:
                gain = len(wholeSet[user])
                chosenUser = user
        chosenSet[chosenUser] = wholeSet.pop(chosenUser)
    return chosenSet

        
# Update the spam score for each user according to their level, assign 1 to the users within the first M levels
def updateSpamScoreI(mthLevel, m, spamScore, gamma, M, retweetUsers, retweetsInM):
    if m <= M:
        for user in mthLevel:
            spamScore[user] = 1
            if m <= M-1:
                for follower in mthLevel[user]:
                    #if follower in spamScore:
                    if follower in retweetUsers:    
                        spamScore[follower] += 1
                        retweetUsers.remove(follower)
                        
def updateSpamScoreII(mthLevel, m, spamScore, gamma, M, retweetUsers, retweetsInM):
    if m <= M:
        for user in mthLevel:
            spamScore[user] += 1
            if m <= M-1:
                for follower in mthLevel[user]:
                    #if follower in spamScore:
                    if follower in retweetUsers:    
                        spamScore[follower] += 1
                        retweetUsers.remove(follower)

# WE assign the spam score by 1/log(1+#retweets)
# Defense III
# We just let all the bots and the retweetUsers retweet the spam, and then calculate their spam score
import math
def updateSpamScoreIII(mthLevel, m, spamScore, gamma, M, retweetUsers, retweetsInM):
    # Let all the bots retweet the spam might be too strong. We need to sample some bots and the legitimate followers to 
    # retweet the tweets
    if m <= M:
        for user in mthLevel:
            spamScore[user] += 1.0 / math.log(1+retweetsInM)
            if m <= M-1:
                for follower in mthLevel[user]:
                    #if follower in spamScore:
                    if follower in retweetUsers:    
                        spamScore[follower] += 1.0 / math.log(1+retweetsInM)
                        retweetUsers.remove(follower)
    '''for user in expNetwork:
        spamScore[user] += 1.0 / math.log(1+len(expNetwork)+len(retweetUsers))
        for follower in expNetwork[user]:
            if follower in retweetUsers:
                spamScore[follower] += 1.0 / math.log(1+len(expNetwork)+len(retweetUsers))
                retweetUsers.remove(follower)
    '''

# Update the spam score for each user according to their level
def updateSpamScoreIV(mthLevel, m, spamScore, gamma, M, retweetUsers, retweetsInM):
    for user in mthLevel:
        spamScore[user] += gamma ** (m - 1)
        for follower in mthLevel[user]:
            #if follower in spamScore and spamScore[follower] == 0:
            #if follower in spamScore:
            if follower in retweetUsers:
                spamScore[follower] += gamma ** m
                # We only allow one spam adding for a legitimate retweeter in a round
                retweetUsers.remove(follower)

'''
Build the retweeting tree by M-level suspension, meaning that the attacker knows
that Twitter will suspend the users within M-1 hops from the source.
expNetwork:
spamScore: 
M: The first M level will be suspended
budget: the number of socialbots that the attacker allows to be suspended
r: retweeting ratio by the  socialbot followers
K: the maximum levels
gamma: the attenuation factor 
retweetUsers: the legitimate retweeters in this round
'''
def spamDistribution(expNetwork, spamScore, M, budget, r, K, gamma, retweetUsers, defenseType):
    if defenseType == 1: updateSpamScore = updateSpamScoreI
    elif defenseType == 2: updateSpamScore = updateSpamScoreII
    elif defenseType == 3: updateSpamScore = updateSpamScoreIII
    elif defenseType == 4: updateSpamScore = updateSpamScoreIV
    
    if len(expNetwork) == 0:
        #print 'Finish!'
        return
    # First choose the minCover with budget socialbots
    firstMLevels = minCover(budget, expNetwork)
    # We need to obtain the number of legitimate followers in this M levels
    legs = set()
    for user in firstMLevels:
        for follower in firstMLevels[user]:
            if follower in retweetUsers: legs.add(follower)
    
    retweetsInM = len(legs)+len(firstMLevels)
    #print len(expNetwork)
    
    # Then choose the M-th level
    MthLevel = maxCover(budget - M + 1, firstMLevels)
    updateSpamScore(MthLevel, M, spamScore, gamma, M, retweetUsers, retweetsInM)
    #updateSpamScoreSusMLevels(MthLevel, m, spamScore, gamma, M)
    # Then choose the socialbots from the first level to the (M-1)-th level
    for m in range(1, M):
        mthLevel = maxCover(1, firstMLevels)
        updateSpamScore(mthLevel, m, spamScore, gamma, M, retweetUsers, retweetsInM)
        #updateSpamScoreSusMLevels(MthLevel, m, spamScore, gamma, M)
        
    # Finally, we choose the socialbots from the (M + 1)-th level to the last one
    lastLevel = MthLevel
    for m in range(M + 1, K):
        # We first obtain the number of socialbots in the m-th level from the m-1 level
        x = 0
        for user in lastLevel:
            x += len(lastLevel[user])
        x = int(1.0 * x * r / (1 - r))
        
        mthLevel = maxCover(x, expNetwork)
        if len(mthLevel) > 0:
            updateSpamScore(mthLevel, m, spamScore, gamma, M, retweetUsers, retweetsInM)
            #updateSpamScoreSusMLevels(MthLevel, m, spamScore, gamma, M)
            lastLevel = mthLevel
        else:
            break
    
    # For the remaining socialbots, we will add them to the level K
    updateSpamScore(expNetwork, K, spamScore, gamma, M, retweetUsers, retweetsInM)
    #updateSpamScoreSusMLevels(MthLevel, K, spamScore, gamma, M)

from operator import add
# DefenseType:
# I: the original M level defense
# II: the one with M levels and suspension when there are M retweets
# III: just consider the number of retweets: 1/ log(1+#retweets)
# IV: our scheme 
def OneExp(n, F, M, budget, r, K, gamma, rtRatio, expRounds, defenseType):
    
    # Consider the randomness of experiment, we repeat each experiment for many times
    # Use this table to record the result
    susRatio = []
    susRatioLeg = []
    
    exptimes = 100
    
    threshold = M if defenseType == 2 else 1.0
    
    for _ in range(1, exptimes + 1):
        susRatioTmp = []
        susRatioLegTmp = []
        
        #print 'Random experiment', exptime
       
        [expNetwork, spamScore] = networkBuild(n, F, 32, 5, rtRatio)
       
        ''' 
        [expNetwork, spamScore] = networkBuild(n, F, 32, 5)
        # We then build a list containing the legitimate users that will rewteet the spam
        followerList = range(n + 1, n + F + 1)
        retweetUsers = random.sample(followerList, int(F * rtRatio))
        for user in retweetUsers:
            if user not in spamScore:
                spamScore[user] = 0
        '''
        # We do many rounds of experiment
        #expRounds = 10
        for _ in range(0, expRounds):
            #print 'This is the ', ro, 'round of experiment'
            workNetwork = dict()
            for user in expNetwork:
                workNetwork[user] = expNetwork[user]
            
            # Re-select the retweeting list
            retweetUsers = chooseLegRetweeters(n, F, 1.0 * rtRatio, spamScore)
            
            spamDistribution(workNetwork, spamScore, M, budget, r, K, gamma, retweetUsers, defenseType)
            
            for user in spamScore:
                if spamScore[user] >= threshold:
                    if user in expNetwork:
                        #print user, spamScore[user]
                        expNetwork.pop(user)
            
            #print 'after this round:', len(expNetwork)
            #print ro, 1.0 * (n - len(expNetwork)) / n
            susRatioTmp.append(1.0 * (n - len(expNetwork)) / n)
            
            # Finally, we record the suspension of the legitimate users:
            susLegitUsers = 0
            for user in spamScore.keys():
                if user > n and spamScore[user] >= threshold:
                    #print user, ro, spamScore[user]
                    susLegitUsers += 1
                    #RuntimeError: dictionary changed size during iteration. We use keys()
                    #spamScore.pop(user)
            #print exptime, ro, susLegitUsers
            susRatioLegTmp.append(1.0 * susLegitUsers / F)
        #print 'Random experiment', exptime, susRatioTmp
        # The first experiment time
        if len(susRatio) == 0:
            for ratio in susRatioTmp:
                susRatio.append(ratio)
        else:
            susRatio = map(add, susRatio, susRatioTmp)

        if len(susRatioLeg) == 0:
            for ratio in susRatioLegTmp:
                susRatioLeg.append(ratio)
        else:
            susRatioLeg = map(add, susRatioLeg, susRatioLegTmp)
            
    #print 'Final Result:', susRatio, map(lambda x : x/10, susRatio)
    return map(lambda x : x/exptimes, susRatio), map(lambda x : x/exptimes, susRatioLeg)


n = 400         # The number of socialbots
F = 6000        # The number of legitimate followers
M = 3       # The users below this level will be completely suspended 
budget = 10     # The number of socialbots that will be suspended
r = 0.2         # The retweeting ratio
K = 10          # The maximum height of the retweeting trees
gamma = 0.7     # The attenuation factor
rtRatio = 0.01   # The probability of a legitimate user retweeting a spam
expRounds = 10

'''
# First we evaluate the impact of gamma
stringSus = ''
stringSusLeg = ''
for gammaTmp in [0.5, 0.6, 0.7, 0.8, 0.9]:
    sus,susLeg = OneExp(n, F, M, budget, r, K, gammaTmp, rtRatio, expRounds, 2)
    print gammaTmp, sus
    print gammaTmp, susLeg
    stringSus += str(sus) + '\n'
    stringSusLeg += str(susLeg) + '\n'
print stringSus
print stringSusLeg
'''

# We then compare our method with others
print "--------------Experiment for M-----------------"
for defenseType in range(1, 5):
    stringSus = ''
    stringSusLeg = ''
    print 'For defense', defenseType
    for m in [1, 2, 3, 9]:
        sus,susLeg = OneExp(n, F, m, budget, r, K, gamma, rtRatio, expRounds, defenseType)
        print m, sus
        print m, susLeg
        stringSus += " ".join([str(x) for x in sus]) + '\n'
        stringSusLeg += " ".join([str(x) for x in susLeg]) + '\n'
    print "TP\n" + stringSus
    print "FP\n" + stringSusLeg


# Finally we evaluate the impact of defense on the performance
print "--------------Experient for Beta-----------------"
for defenseType in range(1, 5):
    stringSus = ''
    stringSusLeg = ''
    print 'For defense', defenseType
    for rtr in [0.01, 0.05, 0.1]:
        sus,susLeg = OneExp(n, F, M, budget, r, K, gamma, rtr, expRounds, defenseType)
        print rtr, sus
        print rtr, susLeg
        stringSus += " ".join([str(x) for x in sus]) + '\n'
        stringSusLeg += " ".join([str(x) for x in susLeg]) + '\n'
    print "TP\n" + stringSus
    print "FP\n" + stringSusLeg