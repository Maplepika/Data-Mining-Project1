# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 02:17:39 2018

@author: neilp
"""

class treeNode:
    def __init__(self,nameValue, numOccur, parentNode):
        self.name= nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
        
    def inc(self, numOccur):
        self.count += numOccur
        
    def disp(self, ind = 1):
        print("Index:", ind, "=>", self.count, "-", self.name)
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet, minSup = 1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item]= headerTable.get(item,0)+dataSet[trans]
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0: return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree= treeNode("NUll Set", 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems =[v[0] for v in sorted(localD.items(),key = lambda p:p[1], reverse= True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)
        
def updateHeader(nodeToTest, targetNode):
    while(nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode
    
def createInitSet(data):
    retDict= {}
    for trx in data:
        retDict[frozenset(trx)] = 1
    return retDict

def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(),key = lambda p: p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)





#test = [['r','z','h','j','p'],['z','y','x','w','v','u','t','s'],['z'],['r','x','n','o','s'],['y','r','x','z','q','t','p'],['y','z','x','e','q','s','t','m']]
IBM_test = [[1,4,5,6,7,8,9],[0,3,4,6,8,9],[0,1,3,8,9],[3,7],[3,5,6,8],[0,8],[0,1,3,7,8,9],[0,3,4,6,7,8,9],[2,3,5,8]]
IS = createInitSet(IBM_test)
tree, tab = createTree(IS, 3)

tree.disp()

path0 = findPrefixPath(0, tab[0][1])
path1 = findPrefixPath(1, tab[1][1])
#path2 = findPrefixPath(2, tab[2][1])

path3 = findPrefixPath(3, tab[3][1])
path4 = findPrefixPath(4, tab[4][1])
path5 = findPrefixPath(5, tab[5][1])
path6 = findPrefixPath(6, tab[6][1])
path7 = findPrefixPath(7, tab[7][1])
path8 = findPrefixPath(8, tab[8][1])
path9 = findPrefixPath(9, tab[9][1])

freqItem = []
mineTree(tree, tab, 3, set([]), freqItem)