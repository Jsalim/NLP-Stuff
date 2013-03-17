from numpy import random
from nltk import FreqDist
from collections import defaultdict
from PCFG_util import getSentPOSFD
from PCFG_util import getWordPOSFD

def getRefs(source='treebank',size=500):

    trees = getTrees(source,size)
##    q, revR = makeQandRR(trees)
    return makeQandRR(trees)

def makeQandRR(trees):

    '''Make FDs for POS-Word pairs and POS-SentPart pairs'''
    WordPOSFD = getWordPOSFD(trees) #From wordPOS2FD
    SentPOSFD = getSentPOSFD(trees) #From ParseTrees2FD
    q = makeQ(SentPOSFD,WordPOSFD)
    revR = makeRR(SentPOSFD,WordPOSFD)
    return q, revR

def getTrees(source,size):
    '''Load the trees from source, return first SIZE trees'''
    if source=='treebank':
        from nltk import treebank
        trees = treebank.parsed_sents()
        #inds = random.permutation(range(0,len(trees)))[0:size]
        trees = trees[:size]
        return trees
    else:
        return list()

def makeQ(SentPOSFD,WordPOSFD):
    '''
    Creates the dictionary 'q' to look up counts of both
    X --> YZ transitions, POS --> word transitions, and
    total counts for both X and POS ((X,*,*) and ('w',POS),
    respectively).  Not the 'True q', but works none-the-less.
    '''
    q = dict()  #Transform Sent and Word into dicts, update q
    q.update(dict(SentPOSFD))
    q.update(dict(WordPOSFD))
    return q

def makeRR(SentPOSFD,WordPOSFD):
    '''
    Creates dictionary for looking up both X's giving rise
    to a particular YZ split, and POS tags associated with
    a particular word.
    '''
    revR = defaultdict(list)
    for X,Y,Z in SentPOSFD.keys():
        revR[(Y,Z)].append(X)
    for POS,w in WordPOSFD.keys():
        if POS!='w':
            revR[w].append(POS)
    return dict(revR)

def POSword_qFD(WordPOSFD):    #checked, works --> only counts!!
    '''
    Construct the initial 'q' dictionary for the
    POS-word pairs in the training data set. Keys
    are (POS,word,-1) tuples, and values are the
    counts of number of times each POS is
    observed with the word.
    '''
    q_list = list()
    for POS_w in WordPOSFD.keys():
        q_list.append((POS_w[0],POS_w[1],-1))
    return FreqDist(q_list)

def POSword_revR(WordPOSFD):     #checked, works
    '''
    Contrsuct the initial 'revR' dictionary for
    POS-word pairs in the training document. Keys
    are words, and values are the list of POS tags
    observed for the word in the training set.
    '''
    revR = defaultdict(list)
    #Get counts for each POS-word tag and
    #number of times each POS tag appears(?)
    for POS_w in WordPOSFD.keys():
        revR[POS_w[1]].append(POS_w[0])      
    return dict(revR)
