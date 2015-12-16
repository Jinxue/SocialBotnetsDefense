'''
Created on Mar 18, 2015

@author: Jinxue Zhang
'''

'''
Build the local following networks after crawling all the friends of the users
'''
import os
from sets import Set

def buildLocalFriends():
    
    dataPath = srcPath + 'result2\\data\\'
    #dataPath = 'E:\\UserDiscover\\TS\\CandidatesCrawling\\Friends\\'

    nodeFile = srcPath + 'gt-refine.txt'
    
    outf = open (resPath + 'friends-local.txt', 'w')
    
    WholeList = Set([])
    
    for line in open(nodeFile, 'rb'):
        node = line.split()
        WholeList.add(node[0])
    print 'Total users:' , len(WholeList)
    
            
    users = 0
    localFriends = 0
    friends = 0
    inputList = os.listdir(dataPath)
    tmpSet = Set()
    
    upperFriends = 100000
    
    numUpperFriends = 0
    
    for ifName in inputList:
        if ifName.startswith('Friends-gt') == False:
        #if ifName.startswith('CrawlTweets-SF11-402057202.txt') == False:
            continue
    
        print ifName
        # We use the binary mode to avoid the unexpected EOF in the middle of the file
        in_f = open(dataPath + ifName, 'rb') 
        for line in in_f:
    
            label = line[0] # this scheme is faster than startswith()       
            
            if label == '%':
                words = line.split(', ')
                #print line
                #print friends, len(tmpSet)
                #print words[0][1:] + "," + str(friends) + "," + str(localFriends)
                # We only include the users in the whole list
                if words[0][1:] not in WholeList:
                    localFriends = 0
                    friends = 0
                    tmpSet.clear()
                    continue
                
                #print line
                if friends > upperFriends:
                    numUpperFriends += 1
                    #localFriends = 0
                    #friends = 0
                    #tmpSet.clear()
                    #continue
                    
                print >> outf, words[0] + "," + str(friends) + "," + str(localFriends)
                for usr in tmpSet:
                    print >> outf, usr
                users += 1
                if users % 10000 == 0:
                    print users * 1.0 / 10000, " 10000 users analyzed."
                    #print numUpperFriends, " users with more than ", upperFriends, "upper followers."
                localFriends = 0
                friends = 0
                tmpSet.clear()
            else:
                friends += 1
                if line.rstrip('\r\n') in WholeList:
                    #outf.write(line)
                    #tmpString += line
                    tmpSet.add(line.rstrip('\r\n'))
                    localFriends += 1
    outf.close()

    
def buildLocalFollowers():
    
    dataPath = srcPath + 'result2\\data\\'
    #dataPath = 'E:\\UserDiscover\\TS\\CandidatesCrawling\\'
    
    nodeFile = srcPath + 'gt-refine.txt'
    
    outf = open (resPath + 'followers-local.txt', 'w')
    
    WholeList = Set([])
    
    for line in open(nodeFile, 'rb'):
        node = line.split()
        WholeList.add(node[0])
    print 'Total users:' , len(WholeList)
    
            
    users = 0
    localFriends = 0
    friends = 0
    inputList = os.listdir(dataPath)
    tmpSet = Set()
    
    upperFriends = 100000
    
    numUpperFriends = 0
    
    for ifName in inputList:
        if ifName.startswith('Followers-gt') == False:
        #if ifName.startswith('CrawlTweets-SF11-402057202.txt') == False:
            continue
    
        print ifName
        # We use the binary mode to avoid the unexpected EOF in the middle of the file
        in_f = open(dataPath + ifName, 'rb') 
        for line in in_f:
    
            label = line[0] # this scheme is faster than startswith()       
            
            if label == '%':
                words = line.split(', ')
                #print line
                #print friends, len(tmpSet)
                #print words[0][1:] + "," + str(friends) + "," + str(localFriends)
                # We only include the users in the whole list
                if words[0][1:] not in WholeList:
                    localFriends = 0
                    friends = 0
                    tmpSet.clear()
                    continue
                
                #print line
                if friends > upperFriends:
                    numUpperFriends += 1
                    #localFriends = 0
                    #friends = 0
                    #tmpSet.clear()
                    #continue
                    
                print >> outf, words[0] + "," + str(friends) + "," + str(localFriends)
                for usr in tmpSet:
                    print >> outf, usr
                users += 1
                if users % 10000 == 0:
                    print users * 1.0 / 10000, " 10000 users analyzed."
                    #print numUpperFriends, " users with more than ", upperFriends, "upper followers."
                localFriends = 0
                friends = 0
                tmpSet.clear()
            else:
                friends += 1
                if line.rstrip('\r\n') in WholeList:
                    #outf.write(line)
                    #tmpString += line
                    tmpSet.add(line.rstrip('\r\n'))
                    localFriends += 1
    outf.close()

def extractInteraction():
    dataPath = srcPath + 'result2\\data\\'
    
    nodeFile = srcPath + 'gt-refine.txt'
    
    out_f = open (resPath + 'interactions-local.txt', 'w')
    
    WholeList = Set([])
    
    for line in open(nodeFile, 'rb'):
        node = line.split()
        WholeList.add(node[0])
    print 'Total users:' , len(WholeList)
    
    
    userName = '' 
    totalInter = 0
    locInter = 0
    
    maxTweetsPerUser = 600
    isLoc = False
    tweetsPerUser = 0
    totalUsers = 0
    locUsers = 0
    tmpSet = dict()
    
    #alreadyGot = False
    inputList = os.listdir(dataPath)
    for ifName in inputList:
        print ifName
        if ifName.startswith('CrawlTweets-gt') == False:
        #if ifName.startswith('CrawlTweets-SF11-402057202.txt') == False:
            continue
    
        # We use the binary mode to avoid the unexpected EOF in the middle of the file
        in_f = open(dataPath + '\\' + ifName, 'rb') 
        for line in in_f:
    
            label = line[0] # this scheme is faster than startswith()       
            #print line
            if label == '%':
                words = line.split(', ')
                userName = words[0][1:].rstrip('\r\n')
                if len(words) == 1:
                    totalInter = 0
                    locInter = 0
    
                    tweetsPerUser = 0
                    if userName in WholeList:
                        isLoc = True
                    else:
                        isLoc = False
                    tmpSet.clear()
                    totalUsers += 1
                    if totalUsers % 10000 == 0:
                        print totalUsers, "users analyzed in the interaction network."
                elif len(words) == 3 and isLoc:
                    if locInter > 0:
                        print >>out_f, "%" + userName + "," + str(totalInter) + "," + str(len(tmpSet)) + "," + str(locInter)
                        for user in tmpSet:
                            print >> out_f, user + "," + str(tmpSet[user])
                    locUsers += 1
                    if locUsers % 10000 == 0:
                        print locUsers, " local users have found."
                    continue 
            elif label == '-' or label == '#': # End of a user or the file
                continue
            elif isLoc :            
                # status_ID::ReplyInStatusID::ReplyInUserID::RetweetCount::RetweetInStatusID::MentionEnt::URLEnt::Text::Time::App:geocode
                #if alreadyGot:
                #    continue 
                tweetsPerUser += 1
                if tweetsPerUser >= maxTweetsPerUser:
                    continue
    
                words = line.split('::')
                if len(words) < 11:
                    #print line
                    #print words
                    #print 'error'
                    pass
                elif words[5] != '-1': 
                    if words[8] == '' or words[8][0].isdigit() == False:
                        continue
                    elif words[8][0] == ':':
                        words[8] = words[8][1:]
                        
                    #We then check whether it is an internal interaction
    
                    mentions = words[5].split(',')
                    #weight = 1.0 / (len(mentions) - 1)
                    weight = 1
                    replyorretweet = 1
                    # First, we will filter out the reply type
                    if words[2] != "-1": 
                        replyorretweet = 2
                        
                        ############################################################################################
                        ## The difference between the 'is not/is' and the '=='
                        ## The 'is' is the identity test for two objects, while '==' is the equality test
                        ## Thus here mentions[1] and userName are euqal but not identical objects
                        ############################################################################################
                        if mentions[1] in WholeList and mentions[1] != userName:
                            #print >>out_f, userName, words[2], words[3], mentions[1], words[8], weight, 0
                            if mentions[1] in tmpSet:
                                tmpSet[mentions[1]] = tmpSet[mentions[1]] + weight
                            else:
                                tmpSet[mentions[1]] = weight
                            locInter += weight
                        if  mentions[1] != userName:
                            totalInter += weight
                    # Second, we will filter out the retweet type
                    #elif words[3] != "0":
                    elif words[4] != "-1":
                        replyorretweet = 2
                        
                        #We ignore the retweet
                        #continue
                        if mentions[1] in WholeList and mentions[1] != userName:
                            #print >>out_f, userName, words[2], words[3], mentions[1], words[8], weight, 1
                            if mentions[1] in tmpSet:
                                tmpSet[mentions[1]] = tmpSet[mentions[1]] + weight
                            else:
                                tmpSet[mentions[1]] = weight

                            locInter += weight
                        if  mentions[1] != userName:
                            totalInter += weight
                    # Finally, all else are the mention type
                    #else:
                    # No 'else' here, we need to collect or the mentions.
                    for mention in mentions[replyorretweet:]:
                        if mention in WholeList  and mention != userName:
                            #print >>out_f, userName, words[2], words[3], mention, words[8], weight, 2
                            #print userName + ',' + words[2] + ',' + words[3] + words[5] + ',' + words[8] + '\r\n'
                            if mention in tmpSet:
                                tmpSet[mention] = tmpSet[mention] + weight
                            else:
                                tmpSet[mention] = weight
                            
                            locInter += weight
                        if mention != userName:
                            totalInter += weight
    
    out_f.close()

def addSeedFiles(path):
    seedFile = path + 'geo.txt'
    candidateFile = path + 'candidates.txt'
    
    outf = open (path + 'candidates-friends-filter.txt', 'a')
    
    WholeList = Set([])
    for line in open(seedFile, 'rb'):
        node = line.rstrip('\r\n')
        WholeList.add(node)
    print '# Seeds:' , len(WholeList)
    
    for line in open(candidateFile, 'rb'):
        node = line.split()
        WholeList.add(node[0])
    print '# Seeds + Candidates:' , len(WholeList)

    users = 0
    localFriends = 0
    friends = 0
    tmpSet = Set()
    
    upperFriends = 10000
    
    numUpperFriends = 0

    for line in open(path + 'Friends-geo.txt'):

        label = line[0] # this scheme is faster than startswith()       
        
        if label == '%':
            words = line.split(', ')
            #print line
            #print friends, len(tmpSet)
            #print words[0][1:] + "," + str(friends) + "," + str(localFriends)
            # We only include the users in the whole list
            if words[0][1:] not in WholeList:
                localFriends = 0
                friends = 0
                tmpSet.clear()
                continue
            
            #print line
            if friends > upperFriends:
                numUpperFriends += 1
                #localFriends = 0
                #friends = 0
                #tmpSet.clear()
                #continue
                
            print >> outf, words[0] + "," + str(friends) + "," + str(localFriends)
            for usr in tmpSet:
                print >> outf, usr
            users += 1
            if users % 10000 == 0:
                print users * 1.0 / 10000, " 10000 users analyzed."
                print numUpperFriends, " users with more than ", upperFriends, "upper followers."
            localFriends = 0
            friends = 0
            tmpSet.clear()
        else:
            friends += 1
            if line.rstrip('\r\n') in WholeList:
                #outf.write(line)
                #tmpString += line
                tmpSet.add(line.rstrip('\r\n'))
                localFriends += 1
    outf.close()


def getMetaInfo(localFile):
    outf = open(localFile.split(".")[0] + "-stat.txt", 'w')
    users = 0
    for line in open(localFile, 'r'):
        if line[0] == '%':
            outf.write(line[1:])
            users += 1
            if users % 10000 == 0:
                print users * 1.0 / 10000, " 10000 users analyzed."
    
dataset = 'TS'
#path = 'L:\\UserDiscover\\CandidateCrawling\\' + dataset + '\\'
#path = 'E:\\UserDiscover\\' + dataset + '\\CandidatesCrawling\Friends\\'
srcPath = 'E:\\UserDiscover\\New\\' + dataset + '\\'
resPath = 'E:\\BotnetDefense\\' + dataset + '\\'
buildLocalFollowers()
buildLocalFriends()
extractInteraction()
#path = 'E:\\UserDiscover\\' + dataset + '\\'
#addSeedFiles(path)
#getMetaInfo(path + 'candidates-filter-whole.txt')