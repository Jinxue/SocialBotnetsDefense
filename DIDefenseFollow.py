'''
Created on Mar 19, 2015

@author: defense for the digital influence measurement
'''

'''
First, we load the file as a dictionary to load the data directly
'''
from sets import Set
def dataLoad():
    # We first need to build a friendSet and creditDict to record all the nodes in the network
    # Note that these nodes may not appear in the users started with % in the friends-local.txt
    for line in open(nodeF, 'r'):
        node = line.rstrip('\r\n')
        friendSet[node] = Set()
        creditDict[node] = 0
    
    #edges = 0
    for line in open(inputF, 'r'):
        if line.startswith('%'):
            items = line.rstrip('\r\n').split(',')
            if len(items) < 3:
                print line
                continue
            else:
                srcid = items[0][1:]
                #friendSet[srcid] = Set()
                #creditDict[srcid] = 0
        else:
            friendSet[srcid].add(line.rstrip('\r\n'))
        '''if edges % 1000000 == 0:
            print 'finished loading ', edges, 'edges.'
        edges += 1
        '''
    totalEdges = 0
    for user in friendSet:
        totalEdges += len(friendSet[user])    
    #print 'Finish the graph building.'
    #print len(friendSet), totalEdges
    return totalEdges

'''
This is the random attack, meaning that the socialbots will randomly choose the targets
'''
def addAttackEdges():
    # First, we build a socialbot with the same number of original network
    botsnum = len(friendSet)
    bots = Set()
    for a in range(1, botsnum):
        bots.add('a' + str(a))
    #print 'Finish adding the socialbots', len(bots)
    
    # Then we randomly choose certain following edges from the legitimate users to the bots
    # In this attack, the socialbots will not be followed by the seeds
    targetedUsers = Set(friendSet.keys()).difference(Set(seedLevel.keys()))
    for _ in range(0, attackedges):
        src = random.sample(targetedUsers, 1)[0]
        dst = random.sample(bots, 1)[0]
        creditDict[dst] = 0
        friendSet[src].add(dst)
        friendSet[dst] = Set()
    #print 'Finish adding the attack edges.'
    
'''
The second attack is for seed attack, meaning that the socialbots will choose the targets among the seeds' neighbors
We choose the targets from the closest nodes from the 100X more than the attack edges  
'''
def addAttackEdges2():
    # First, we build a socialbot with the same number of original network
    botsnum = len(friendSet)
    bots = Set()
    for a in range(1, botsnum):
        bots.add('a' + str(a))
    #print 'Finish adding the socialbots', len(bots)
    
    # Second we build the target set
    if len(friendSet) < 100 * attackedges:
        print 'Error out of bound when building the attack targets!'
        exit() 
    targetedUsers = Set()
    thisLevel = seedLevel.keys()
    while True:
        if len(targetedUsers) < 100 * attackedges:
            if len(targetedUsers) + len(thisLevel) < 100 * attackedges:
                #for user in thisLevel:
                    #if user in friendSet:
                #    targetedUsers.add(user)
                targetedUsers.update(thisLevel)
            else:
                #for user in random.sample(thisLevel, 100 * attackedges - len(targetedUsers)):
                    #if user in friendSet:
                #    targetedUsers.add(user)
                targetedUsers.update(random.sample(thisLevel, 100 * attackedges - len(targetedUsers)))
        else:
            break
        nextLevel = Set()
        for user in thisLevel:
            #if user in friendSet:
            #for friend in friendSet[user]:
            #    nextLevel.add(friend)
            nextLevel.update(friendSet[user])
        thisLevel = nextLevel
    #print 'Finish building the targets', len(bots)
            
    # Then we randomly choose certain following edges from the legitimate users to the bots
    # In this attack, the socialbots will not be followed by the seeds
    #targetedUsers = Set(friendSet.keys()).difference(Set(seedLevel.keys()))
    for _ in range(0, attackedges):
        src = random.sample(targetedUsers, 1)[0]
        dst = random.sample(bots, 1)[0]
        creditDict[dst] = 0
        friendSet[src].add(dst)
        friendSet[dst] = Set()
    #print 'Finish adding the attack edges.'

'''
Then we distribute the credits from the seeds
The idea is to maintain a table to record the credits for each user.

Each seed will obtain [sqrt(n)] credits as the initial credits.
If a node u receives n credits, he will hold one for himself, and then send
[(n-1) / nout] to his nout friends. To deal with the decimal, we randomly
choose n - [(n-1) / nout] friends and send each of them one credit.

Two special cases:
1. if the user has no friends, his credits will be discarded
2. if the user has only one credit, he will hold this credit and not send it again
3. No backstrap is allowed in the credit distribution
4. at the same level, the user could receive credits from multiple followers
'''
import math, random
def creditDistrition():
    level = 1
    #sendLevel = findSeeds1()
    sendLevel = seedLevel
    # load the seeds as the first level
    while True:
        #print 'we are now at level', level, 'with users', len(friendSet)
        level += 1
        
        if len(sendLevel) == 0:
            #print 'Credit distribution finished!'
            break
        
        receiveLevel = dict()
        
        nextLevel = Set(friendSet.keys()).difference(Set(sendLevel.keys()))
        # Now we do the credit distribution
        for user in sendLevel:
            
            # We don't allow the backstrap
            friends = friendSet.pop(user)
            effFriends = friends.intersection(nextLevel)
            
            if sendLevel[user] < 1:
                continue
            # If the user is a socialbot, we will hold all the credits; otherwise, we will just assign one credit for it
            if user.startswith('a'):
                creditDict[user] = sendLevel[user]
            else:
                creditDict[user] = 1
            # If the user has no friends, we just end the credit distribution
            if len(effFriends) == 0:
                #print 'User', user, 'has zero friends in the next level'
                continue
            
            # For each friend, we will have the same basic credits
            basicCredits = (sendLevel[user] - 1) / len(effFriends)
            extraCredits = (sendLevel[user] - 1) % len(effFriends)
            
            for friend in effFriends:
                if friend in receiveLevel:
                    receiveLevel[friend] += basicCredits
                else:
                    receiveLevel[friend] = basicCredits
            # We then handle the extra credits in this level.
            # We randomly select extarCredits users and assigan each of them one credit
            if extraCredits > 0:
                selected = random.sample(effFriends, extraCredits)
                for friend in selected:
                    receiveLevel[friend] += 1
        sendLevel = receiveLevel
        
    # We then record the users with the credits
    userswithcredits = 0
    botswithcredits = 0
    for user in creditDict:
        if creditDict[user] >= 1:
            if user.startswith('a'):
                botswithcredits += creditDict[user]
            else:
                userswithcredits += creditDict[user]
                effUsers.add(user)
    
    #print userswithcredits, 'users with credits.', botswithcredits, 'bots with credits.', 'with attack edges', attackedges
    
    return botswithcredits

'''
We have different ways to find the seeds
1. Using the verified users
2. By fixed ratio of random selection
'''
def findSeeds1():
    # For each seed, we will assign sqrt(n) credits initially
    initcredits = int(math.ceil(math.sqrt(len(friendSet))))
    
    seedFromFile = Set()
    for line in open(seedsF, 'r'):
        seedFromFile.add(line.rstrip('\r\n'))
    #seeds = random.sample(seedFromFile, initcredits)
    #seeds = Set()
    if len(seedFromFile) < initcredits:
        seeds =Set(seedFromFile)
        for user in random.sample(friendSet.keys(), initcredits - len(seedFromFile)):
            seeds.add(user)
    else:
        seeds = Set(random.sample(seedFromFile, initcredits))
        
    for user in seeds:
        seedLevel[user] = int(math.ceil(70))
    #print 'We have ', len(seedLevel), 'seeds as the first level'
    return seedLevel

def findSeeds2():
    initcredits = int(math.ceil(math.sqrt(len(friendSet))))
    seeds = random.sample(friendSet.keys(), initcredits)
    
    totalNeighbors = 0
    for seed in seeds:
        #print seed, len(friendSet[seed])
        totalNeighbors += len(friendSet[seed])
    print 'We have total neighbors from the seeds', totalNeighbors
    for seed in seeds:
        #seedLevel[seed] = initcredits
        seedLevel[seed] = int(math.ceil(0.5 * len(friendSet) * len(friendSet[seed]) / totalNeighbors))
    print 'We have ', len(seedLevel), 'seeds as the first level'
    return seedLevel
    
'''
Finally we obtain the performance results
We will measure two metrics:
1. Accuracy: what is the impact of credit distribution on legitimate users ranking? To that end, we rank the legitimate users
before and after the distribution and then calculate their difference.
2. Defense against social botnets: which level could social botnets manipulate their ranking? To that end, we compute the
ranking that a socialbot could achieve after the credit distribution. 
'''
def perfResults(r, botswithcredits):
    #print '####### Measuring the results'
    #edges = 0
    # We first need to build a friendSet and creditDict to record all the nodes in the network
    # Note that these nodes may not appear in the users started with % in the friends-local.txt
    friendSet = dict()
    origInfluence = dict()
    refInfluence = dict()
    for line in open(nodeF, 'r'):
        node = line.rstrip('\r\n')
        friendSet[node] = Set()
        origInfluence[node] = 0
        refInfluence[node] = 0
    
    # We then define the original and refined influence score for each user
    for line in open(influenceF):
        if line.startswith('%'):
            items = line.rstrip('\r\n').split(',')
            if len(items) < 3:
                print line
                continue
            else:
                srcid = items[0][1:]
                #friendSet[srcid] = Set()
                origInfluence[srcid] = int(items[2])
        else:
            friendSet[srcid].add(line.rstrip('\r\n'))
        '''if edges % 1000000 == 0:
            print 'finished computing ', edges, 'edges.'
        edges += 1
        '''
    for user in friendSet:
        refInfluence[user] = len(friendSet[user].intersection(effUsers))
    # ranking
    orig_ordered = rankWithRepeat(origInfluence)
    ref_ordered = rankWithRepeat(refInfluence)
    ref_ordered_dict = OrderedDict(ref_ordered)
    
    # We only report the difference for the top Kratio users
    topK = int(r * len(origInfluence))
    diff1 = 0
    topK1 = Set()
    topK2 = Set()
    for i in range(0, topK):
        user,value = orig_ordered[i]
        diff1 += abs(value-ref_ordered_dict[user])
        topK1.add(user)
        topK2.add(ref_ordered[i][0])
    #err=sum([abs(value-ref_ordered[user]) for user,value in orig_ordered])

    diff2 = topK - len(topK1.intersection(topK2))    
    #print 'Legitimate users of top ', topK, 'users have the average difference of ', 1.0 * diff1 / topK, \
    #     'the second type of difference', 1.0 * diff2 / topK
    
    # we also report the ranking for the sybil users
    ref_list = sorted(refInfluence.items(), key=lambda x: x[1], reverse=True)
    for ii in range(1, len(ref_list) + 1):
        _,value = ref_list[ii - 1]
        if botswithcredits >= value:
            botRank = ii
            break
    #print 'Social botnets could rank at most ', botRank, 1.0 * botRank / len(friendSet) 
    
    '''
    outf = open(path + 'ranking-following.txt', 'w')
    for user,value in orig_ordered:
        print >>outf, user, value, ref_ordered_dict[user], origInfluence[user], refInfluence[user]
    '''
    return 1.0 * diff1 / topK, 1.0 * diff2 / topK, botRank, 1.0 * botRank / len(friendSet) 
  
def perfResultsForMultipleKs(outF, dataset, expRound, res, botswithcredits):
    #print '####### Measuring the results'
    #edges = 0
    #friendSet = dict()
    # We first need to build a friendSet and creditDict to record all the nodes in the network
    # Note that these nodes may not appear in the users started with % in the friends-local.txt
    friendSet = dict()
    origInfluence = dict()
    refInfluence = dict()
    for line in open(nodeF, 'r'):
        node = line.rstrip('\r\n')
        friendSet[node] = Set()
        origInfluence[node] = 0
        refInfluence[node] = 0
    
    # We then define the original and refined influence score for each user
    for line in open(influenceF):
        if line.startswith('%'):
            items = line.rstrip('\r\n').split(',')
            if len(items) < 3:
                print line
                continue
            else:
                srcid = items[0][1:]
                #friendSet[srcid] = Set()
                origInfluence[srcid] = int(items[2])
        else:
            friendSet[srcid].add(line.rstrip('\r\n'))
        '''if edges % 1000000 == 0:
            print 'finished computing ', edges, 'edges.'
        edges += 1
        '''
    for user in friendSet:
        refInfluence[user] = len(friendSet[user].intersection(effUsers))
    # ranking
    orig_ordered = rankWithRepeat(origInfluence)
    ref_ordered = rankWithRepeat(refInfluence)
    ref_ordered_dict = OrderedDict(ref_ordered)
    
    # We also report the difference for the top Kratio users
    KRatios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    res2 = []
    for Kratio in KRatios:
        topK = int(Kratio * len(origInfluence))
        diff1 = 0
        topK1 = Set()
        topK2 = Set()
        for i in range(0, topK):
            user,value = orig_ordered[i]
            diff1 += abs(value-ref_ordered_dict[user])
            topK1.add(user)
            topK2.add(ref_ordered[i][0])
        #err=sum([abs(value-ref_ordered[user]) for user,value in orig_ordered])
    
        diff2 = topK - len(topK1.intersection(topK2))    
        diff1 = 1.0 * diff1 / topK
        diff2 = 1.0 * diff2 / topK
        #print 'Legitimate users of top ', topK, 'users have the average difference of ', 1.0 * diff1 / topK, \
        #     'the second type of difference', 1.0 * diff2 / topK
        res2.append([diff1, diff2])
        
        outf = open(outF, 'a')
        print dataset, Kratio, expRound + 1, diff1,diff2
        print >>outf, dataset, Kratio, expRound + 1, diff1,diff2
        outf.close()
        '''outf = open(path + 'ranking-interaction.txt', 'w')
        for user,value in orig_ordered:
            print >>outf, user, value, ref_ordered_dict[user], origInfluence[user], refInfluence[user]
        '''
    for ii in range(0, len(KRatios)):
        a,b = res2[ii]
        if len(res) != len(KRatios):
            res.append([a, b])
        else :
            a1,b1 = res[ii]
            res[ii] = [a + a1, b + b1]
        

'''
We define this method to rank a dictionay by value, and output a new dictionary with the ranking value by decreasing.
If two or more items have the same value, we will assign them the same ranking value 
'''
from collections import OrderedDict
def rankWithRepeat(rawDict):
    ordered = sorted(rawDict.items(), key=lambda x: x[1], reverse=True)
    
    ranking = []
    x = 1
    lastRank = 1
    lastValue = -1
    for user,value in ordered:
        if value != lastValue:
            thisRank = x
            lastRank = x
        else:
            thisRank = lastRank
        
        lastValue = value
        ranking.append([user, thisRank])
        x += 1
    return ranking

'''
We conduct the experiment by averaging 100 rounds
'''
print 'This is the results for following network at dataset'
expRounds = 100

'''
print 'Attack I'
outF = 'E:\\BotnetDefense\\results-following-attack1.txt'
for dataset in ['TS', 'PI', 'CI', 'LA']:
    res1 = []
    for alpha in [0.00001, 0.00002, 0.00003, 0.00004, 0.00005, 0.00006, 0.00007, 0.00008, 0.00009, 0.0001]:
        res2 = []
        for expRound in range(0, expRounds):
            path = 'E:\\BotnetDefense\\' + dataset + '\\'
            nodeF = path + 'gt-refine.txt'
            inputF = path + 'friends-local.txt'
            influenceF = path + 'followers-local.txt'
            #inputF = path + 'interactions-local.txt'
            seedsF = path + 'seeds.txt'
            
            
            # The friend dictionary
            friendSet = dict()
            # Record the credits for each user in the network
            creditDict = dict()
            # Obtain the users with the credits
            effUsers = Set()
            
            # Prepare the seeds for the credit distribution
            seedLevel = dict()
            
            # The ratio of top-K for the ranking
            Kratio = 0.1
            
            totalEdges = dataLoad()
            findSeeds1()
            attackedges = int(alpha * totalEdges)
            addAttackEdges()
            botswithcredits = creditDistrition()
            diff1,diff2,ranking,rankingPer = perfResults(Kratio, botswithcredits)
            
            outf = open(outF, 'a')
            print dataset, alpha, expRound, diff1,diff2,botswithcredits,ranking,rankingPer
            print >>outf, dataset, alpha, expRound, diff1,diff2,botswithcredits,ranking,rankingPer
            outf.close()
            
            res2.append([diff1,diff2,botswithcredits,ranking, rankingPer])
        # Summarize the res2
        diff1 = 0
        diff2 = 0
        botswithcredits = 0
        ranking = 0
        rankingPer = 0
        for a,b,c,d,e in res2:
            diff1 += a
            diff2 += b
            botswithcredits += c
            ranking += d
            rankingPer += e
        res1.append([1.0 * diff1 / expRounds, 1.0 * diff2 / expRounds, 1.0 * botswithcredits / expRounds, \
                      1.0 * ranking / expRounds, 1.0 * rankingPer / expRounds])
    outf = open(outF, 'a')
    print '############ The result for', dataset
    print >>outf, '############ The result for', dataset
    for a,b,c,d,e in res1:
        print a,b,c,d,e
        print >>outf, a,b,c,d,e
    outf.close()
        
print 'Attack II'
outF = 'E:\\BotnetDefense\\results-following-attack2.txt'
#for dataset in ['TS', 'PI', 'CI', 'LA']:
for dataset in ['TS', 'PI', 'CI']:
    res1 = []
    for alpha in [0.00001, 0.00002, 0.00003, 0.00004, 0.00005, 0.00006, 0.00007, 0.00008, 0.00009, 0.0001]:
        res2 = []
        for expRound in range(0, expRounds):
            path = 'E:\\BotnetDefense\\' + dataset + '\\'
            nodeF = path + 'gt-refine.txt'
            inputF = path + 'friends-local.txt'
            influenceF = path + 'followers-local.txt'
            #inputF = path + 'interactions-local.txt'
            seedsF = path + 'seeds.txt'
            
            # The friend dictionary
            friendSet = dict()
            # Record the credits for each user in the network
            creditDict = dict()
            # Obtain the users with the credits
            effUsers = Set()
            
            # Prepare the seeds for the credit distribution
            seedLevel = dict()
            
            # The ratio of top-K for the ranking
            Kratio = 0.1
            
            totalEdges = dataLoad()
            findSeeds1()
            attackedges = int(alpha * totalEdges)
            addAttackEdges2()
            botswithcredits = creditDistrition()
            diff1,diff2,ranking,rankingPer = perfResults(Kratio, botswithcredits)
            
            outf = open(outF, 'a')
            print dataset, alpha, expRound, diff1,diff2,botswithcredits,ranking,rankingPer
            print >>outf, dataset, alpha, expRound, diff1,diff2,botswithcredits,ranking,rankingPer
            outf.close()
            
            res2.append([diff1,diff2,botswithcredits,ranking, rankingPer])
        # Summarize the res2
        diff1 = 0
        diff2 = 0
        botswithcredits = 0
        ranking = 0
        rankingPer = 0
        for a,b,c,d,e in res2:
            diff1 += a
            diff2 += b
            botswithcredits += c
            ranking += d
            rankingPer += e
        res1.append([1.0 * diff1 / expRounds, 1.0 * diff2 / expRounds, 1.0 * botswithcredits / expRounds, \
                      1.0 * ranking / expRounds, 1.0 * rankingPer / expRounds])
    outf = open(outF, 'a')
    print '############ The result for', dataset
    print >>outf, '############ The result for', dataset
    for a,b,c,d,e in res1:
        print a,b,c,d,e
        print >>outf, a,b,c,d,e
    outf.close()
'''

print 'Attack I'
outF = 'E:\\BotnetDefense\\results-following-attack1-topk.txt'
for dataset in ['TS', 'PI', 'CI', 'LA']:
    res1 = []
    #for alpha in [0.00001, 0.00002, 0.00003, 0.00004, 0.00005, 0.00006, 0.00007, 0.00008, 0.00009, 0.0001]:
    for alpha in [0.00005]:
        for expRound in range(0, expRounds):
            path = 'E:\\BotnetDefense\\' + dataset + '\\'
            nodeF = path + 'gt-refine.txt'
            inputF = path + 'friends-local.txt'
            influenceF = path + 'followers-local.txt'
            #inputF = path + 'interactions-local.txt'
            seedsF = path + 'seeds.txt'
            
            
            # The friend dictionary
            friendSet = dict()
            # Record the credits for each user in the network
            creditDict = dict()
            # Obtain the users with the credits
            effUsers = Set()
            
            # Prepare the seeds for the credit distribution
            seedLevel = dict()
            
            # The ratio of top-K for the ranking
            #Kratio = 0.1
            
            totalEdges = dataLoad()
            findSeeds1()
            attackedges = int(alpha * totalEdges)
            addAttackEdges()
            botswithcredits = creditDistrition()
            
            '''
            KRatios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            res2 = []
            for Kratio in KRatios:
                diff1,diff2,ranking,rankingPer = perfResults(Kratio, botswithcredits)
                outf = open(outF, 'a')
                print dataset, Kratio, expRound, diff1,diff2,botswithcredits,ranking,rankingPer
                print >>outf, dataset, Kratio, expRound, diff1,diff2,botswithcredits,ranking,rankingPer
                outf.close()
                
                res2.append([diff1,diff2,botswithcredits,ranking, rankingPer])
            # Summarize the res2 to the res1
            for ii in range(0, len(KRatios)):
                a,b,c,d,e = res2[ii]
                if expRound == 0:
                    res1.append([a,b,c,d,e])
                else:
                    a1,b1,c1,d1,e1 = res1[ii]
                    res1[ii] = [a + a1, b + b1, c + c1, d + d1, e + e1]
            '''
            perfResultsForMultipleKs(outF, dataset, expRound, res1, botswithcredits)
            
    outf = open(outF, 'a')
    print '############ The result for', dataset
    print >>outf, '############ The result for', dataset
    for a,b in res1:
        print 1.0 * a / expRounds, 1.0 * b / expRounds
        print >>outf, 1.0 * a / expRounds, 1.0 * b / expRounds
    outf.close()
        
print 'Attack II'
outF = 'E:\\BotnetDefense\\results-following-attack2-topk.txt'
#for dataset in ['TS', 'PI', 'CI', 'LA']:
for dataset in ['TS', 'PI', 'CI', 'LA']:
    res1 = []
    #for alpha in [0.00001, 0.00002, 0.00003, 0.00004, 0.00005, 0.00006, 0.00007, 0.00008, 0.00009, 0.0001]:
    for alpha in [0.00005]:
        for expRound in range(0, expRounds):
            path = 'E:\\BotnetDefense\\' + dataset + '\\'
            nodeF = path + 'gt-refine.txt'
            inputF = path + 'friends-local.txt'
            influenceF = path + 'followers-local.txt'
            #inputF = path + 'interactions-local.txt'
            seedsF = path + 'seeds.txt'
            
            # The friend dictionary
            friendSet = dict()
            # Record the credits for each user in the network
            creditDict = dict()
            # Obtain the users with the credits
            effUsers = Set()
            
            # Prepare the seeds for the credit distribution
            seedLevel = dict()
            
            # The ratio of top-K for the ranking
            #Kratio = 0.1
            
            totalEdges = dataLoad()
            findSeeds1()
            attackedges = int(alpha * totalEdges)
            addAttackEdges2()
            botswithcredits = creditDistrition()
            
            '''
            KRatios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            res2 = []
            for Kratio in KRatios:
                diff1,diff2,ranking,rankingPer = perfResults(Kratio, botswithcredits)
                
                outf = open(outF, 'a')
                print dataset, Kratio, expRound, diff1,diff2,botswithcredits,ranking,rankingPer
                print >>outf, dataset, Kratio, expRound, diff1,diff2,botswithcredits,ranking,rankingPer
                outf.close()
                
                res2.append([diff1,diff2,botswithcredits,ranking, rankingPer])
            # Summarize the res2 to the res1
            for ii in range(0, len(KRatios)):
                a,b,c,d,e = res2[ii]
                if expRound == 0:
                    res1.append([a,b,c,d,e])
                else:
                    a1,b1,c1,d1,e1 = res1[ii]
                    res1[ii] = [a + a1, b + b1, c + c1, d + d1, e + e1]
            '''
            perfResultsForMultipleKs(outF, dataset, expRound, res1, botswithcredits)
            
    outf = open(outF, 'a')
    print '############ The result for', dataset
    print >>outf, '############ The result for', dataset
    for a,b in res1:
        print 1.0 * a / expRounds, 1.0 * b / expRounds
        print >>outf, 1.0 * a / expRounds, 1.0 * b / expRounds

    outf.close()
