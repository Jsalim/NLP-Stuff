import nltk
from collections import defaultdict

def simp_tag(tag):
    '''Simplifies tags to brown-style'''
    return nltk.tag.simplify_brown_tag(tag)

def word_POS_grab(sents,simple=True):
    '''
    For all sents in the doc, count the number of times
    each POS-word combo appears in the doc.
    '''
    for sent in sents:
        #Grab the POS tag for each word in the sentence tree
        new_wPOSdict = word_POS_grab_sent(sent,simple)
        #Update the overall word-POS dictionary counts
        for tw in new_wPOSdict.keys():
            wPOSdict[tw] = wPOSdict[tw] + new_wPOSdict[tw]
    return wPOSdict

def word_POS_grab_sent(sent,simple):
    '''
    Iterate over items at height 2 in sent tree
    and count number of times each POS-word combo
    appears.  Keys are (POS, word) tuples.
    '''
    wPOSdict = defaultdict(int)
    if simple:
        for s in sent.subtrees(lambda t: t.height() == 2):
            wPOSdict[(simp_tag(s.node),s[0])] =\
            wPOSdict[(simp_tag(s.node),s[0])]+1
    else:
        for s in sent.subtrees(lambda t: t.height() == 2):
            wPOSdict[(s.node,s[0])] =\
            wPOSdict[(s.node,s[0])] + 1
    return wPOSdict

def POSword_q(wPOSdict):
    '''
    Construct the initial 'q' dictionary for the
    POS-word pairs in the training data set. Keys
    are (POS,word,-1) tuples, and values are the
    fraction of the time the observed POS is
    associated with the word.
    '''
    q = defaultdict(int)
    for POS_w in wPOSdict.keys():
        q[(POS_w[0],POS_w[1],-1)] =\
        q[(POS_w[0],POS_w[1],-1)] + wPOSdict[POS_w]
    return dict(q)

def POSword_revR(wPOSdict):
    '''
    Contrsuct the initial 'revR' dictionary for
    POS-word pairs in the training document. Keys
    are words, and values are the list of POS tags
    observed for the word in the training set.
    '''
    revR = defaultdict(list)
    for POS_w in wPOSdict.keys():
        revR[POS_w[1]].append(POS_w[0])
    return dict(revR)
