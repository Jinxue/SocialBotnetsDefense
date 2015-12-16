'''
Created on Mar 19, 2015

@author: Jinxue Zhang
Get the verified users for each location
'''
from sets import Set
for dataset in ['TS', 'PI', 'CI', 'LA']:
    path = 'E:\\BotnetDefense\\'
    
    verifiedF = path + 'verifiedUsers.txt'
    
    usersF = path + dataset + '\\gt-refine.txt'
    
    outF = open(path + dataset + '\\seeds.txt', 'w')
    
    verified = Set()
    num1 = 0
    num2 = 0
    for line in open(verifiedF, 'r'):
        verified.add(line)
         
    for line in open(usersF, 'r'):
        num1 += 1
        if line in verified:
            outF.write(line)
            num2 += 1
    
    print dataset, num1, num2, 1.0 * num2 / num1

