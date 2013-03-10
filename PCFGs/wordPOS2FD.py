import nltk
from collections import defaultdict
from PCFG_util import simp_tag


def getWordPOSFD(sents,simple=True):
    '''
    For all sents in the doc, count the number of times
    each POS-word combo appears in the doc.
    '''
    wPOS_list = list()
    for sent in sents:
        wPOS_list.extend(word_POS_grab_sent(sent,simple))
    wPOSFD = nltk.FreqDist(wPOS_list)
    return wPOSFD

def word_POS_grab_sent(sent,simple):
    '''
    Iterate over items at height 2 in sent tree
    and count number of times each POS-word combo
    appears.  Keys are (POS, word) tuples.
    '''
    if simple:
        wPOSlist = [(simp_tag(s.node),s[0]) for s in \
                    sent.subtrees(lambda t: t.height() == 2)]
    else:
       wPOSlist = [(simp_tag(s.node),s[0]) for s in \
                   sent.subtrees(lambda t: t.height() == 2)]
    return wPOSlist
