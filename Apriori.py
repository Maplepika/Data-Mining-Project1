# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 22:18:55 2018

@author: neilp
"""

def loaddata():
    return [[1,4,5,6,7,8,9],[0,3,4,6,8,9],[0,1,3,8,9],[3,7],[3,5,6,8],[0,8],[0,1,3,7,8,9],[0,3,4,6,7,8,9],[2,3,5,8]]

def createC1(data):
    L = []
    for trx in data:
        for item in trx:
            if not [item] in L:
                L.append([item])
    L.sort()
    return frozenset(map(frozenset, L))

def scandata(data, Ck, minSup):
    ssCnt = {}
    for tid in data:
        for Citem in Ck:
            if Citem.issubset(tid):
                if not Citem in ssCnt:
                    ssCnt[Citem] = 1
                else: 
                    ssCnt[Citem] += 1
    nItems = float(len(data))
    retList = []
    supportData = {}
    for key in ssCnt:
        supportV = ssCnt[key] / nItems
        if supportV >= minSup:
            retList.insert(0,key)
        supportData[key] = supportV
    return retList, supportData

def aprioriGenerate(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i]|Lk[j])
    return retList

def apriori(data, minSupport = 0.5):
    C1 = createC1(data)
    D = list(map(set,data))
    L1, supportData = scandata(D, C1, minSupport)
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0):
        Ck = aprioriGenerate(L[k-2], k)
        Lk, supK= scandata(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def generateRules(L, supData, minConf = 0.7):
    ruleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i > 1:
                rulesFromConseq(freqSet, H1, supData, ruleList, minConf)
            else:
                calConf(freqSet, H1, supData, ruleList, minConf)
    return ruleList

def calConf(freqSet, H, supData, ruleList, minConf = 0.7):
    retH = []
    for conseq in H:
        conf = supData[freqSet] / supData[freqSet - conseq]
        if(conf >= minConf):
            print(freqSet - conseq, "=>", conseq, "conf: ", conf)
            ruleList.append((freqSet - conseq, conseq, conf))
            retH.append(conseq)
    return retH

def rulesFromConseq(freqSet, H, supData, ruleList, minConf = 0.7):
    m = len(H[0])
    if(len(freqSet) > m+1):
        newrule = aprioriGenerate(H, m+1)
        newrule = calConf(freqSet, newrule, supData, ruleList, minConf)
        if(len(newrule)>1):
            rulesFromConseq(freqSet, newrule, supData, ruleList, minConf)
        
#IBM testing
D = loaddata()
C1 = createC1(D)
L, sup = apriori(D, 0.5)
rules = generateRules(L, sup, minConf = 0.7)
