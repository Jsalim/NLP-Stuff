from nltk import FreqDist
from collections import defaultdict

def getRefs(wPOSFD,


def POSword_pre_q(wPOSFD):    #checked, works --> only counts!!
    '''
    Construct the initial 'q' dictionary for the
    POS-word pairs in the training data set. Keys
    are (POS,word,-1) tuples, and values are the
    counts of number of times each POS is
    observed with the word.
    '''
    pre_q = list()
    for POS_w in wPOSdict.keys():
        pre_q.append((POS_w[0],POS_w[1],-1))
    return FreqDist(pre_q)

def POSword_revR(wPOSFD):     #checked, works
    '''
    Contrsuct the initial 'revR' dictionary for
    POS-word pairs in the training document. Keys
    are words, and values are the list of POS tags
    observed for the word in the training set.
    '''
    revR = defaultdict(list)
    #Get counts for each POS-word tag and
    #number of times each POS tag appears(?)
    for POS_w in wPOSdict.keys():
        revR[POS_w[1]].append(POS_w[0])      
    return dict(revR)
