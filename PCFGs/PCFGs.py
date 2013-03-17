import nltk
from collections import defaultdict
##from PCFG_util import rebuildBest
import PCFG_util


def CKY_alg01(sent,G):
    '''
    Carries out CKY algorithm for parsing a senetence, as
    described in PCFGs (M. Collins);
    Given a sentence and a PCFG, G (with components:
    N   --> Set of all non-terminal words in training
    Sig --> Set of all words in training
    S   --> Start symbol
    R   --> Rule set in grammar
        (revR is the reverse lookup for these rules)
    q   --> MLE from training
        (e.g., q(a) = count(a -> b)/count(a).
        qC is a count dictionary, so
        qC((a,b)) = count(a -> b) and qC((a,*) = count(a))
    returns the maximum liklihood parsing...

    'sent' is just a list of words
    '''
    revR = G['revR']
    q = G['q']
    
    '''Senetence specific initialization'''
    tags,scores,bp = initialize_Refs(sent,revR,q)
    
    '''
    This determines the size of the chunk; no word-size
    chunks because we've already visited those when
    initializeing tags, scores, and bp.
    '''
    for l in range(1,len(sent)-1):
        '''This determines the beginning of the chunk'''
        for i in range(0,len(sent)-l):
            '''This determines the end of the chunk'''
            j = l+i
            #This is the part where we take each of the current
            #level tags and attempt to merge into higher-level
            #tags
            tags,scores,bp = CKY_meat01(revR,q,
                                        i,j,
                                        tags,scores,bp)
    '''Retreive the MLE solution'''
    #out = PCFG_util.rebuildBest(len(sent)-1,bp)
    return bp

def CKY_meat01(revR,q,i,j,tags,scores,bp):
    '''
    Non-lexical PCFG method
    
    i is the start of the segment, j is the end of the segment,
    tags is a dictionary with keys i,j such that
    revR is the dictionary of possible rules, keys being (Y,Z)
    and values the list of X's that can break into said Y,Z
    pair.
    
    tags[(i,j)] -> list(current allowed tags for segment [i,j])
    scores is a dictionary of current (i,j,tag) probabilities
    q is a dictionary of probabilitys for X --> YZ splits
    '''
    # (i,j) is not unique; can have multiple associated tags
    # (i,j,tag) is unique --> pi(i,j,X)
    temp_pies = defaultdict(list)
    for s in range(i,j):  
        lft = tags[(i,s)]; rgt = tags[(s+1,j)]
        #If none in one or other, won't add to temp
        for l in lft:
            for r in rgt:
                yProb = scores[(i,s,l)]; zProb = scores[(s+1,j,r)]
                try:
                    Xs = revR[(l,r)]
                    #Need corresponding probability of each Y,Z
                    for x in Xs:
                        temp_pies[x].append((s,l,r,
                                            q((x,l,r))*yProb*zProb))
                except KeyError: pass
    #Update everything and spit back out
    return update_refs(i,j,temp_pies,scores,tags,bp)

def initialize_Refs(sent,revR,q):
    '''Populate bp and scores  with words from the sentence'''
    tags = initialize_tags(sent,revR)
    scores = initialize_scores(sent,q,tags)
    bp = initialize_bp(sent,tags)
    return tags,scores,bp
    
def initialize_scores(sent,q,tags):
    '''
    Initialices the scores dictionary with an entry
    for each (i,i,POS) tuple, i.e., create an entry
    for every POS tag associated with each word as
    the probability of that word having that POS
    '''
    scores = dict()
    for i,w in enumerate(sent):
        for POS in tags[(i,i)]:
            scores[(i,i,POS)] = q((POS,w))
    return scores

def initialize_tags(sent,revR):
    '''
    Initialise 'tags' with the list of observed
    POS tags for each word in the sentence.
    '''
    tags = dict()
    for i,w in enumerate(sent):
        tags[(i,i)] = revR[w]
    return tags

def initialize_bp(sent,tags):
    '''
    Initializes bp with the words in sentence;
    makes an entry for each (word,POS) combo
    '''
    bp = dict()
    for i,w in enumerate(sent):
        for t in tags[(i,i)]:
            bp[(i,i,t)] = w
    return bp

def update_refs(i,j,temp_pies,scores,tags,bp):
    '''
    Update all persistent reference dicts for
    traking progress up the tree
    '''
    new_pies = best_pies(temp_pies)
    scores = update_scores(i,j,scores,new_pies)
    tags = update_tags(i,j,tags,new_pies)
    bp = update_bp(i,j,bp,new_pies)
    return tags,scores,bp

def best_pies(temp_pies):
    '''
    Find best X --> YZ transition for each X occuring
    in the temp_pies
    '''
    new_pies = dict()
    for X in temp_pies.keys():
        vals = [v[-1] for v in temp_pies[X]]
        which = vals.index(max(vals))
        new_pies[X] = temp_pies[X][which]
    return new_pies

def update_scores(i,j,scores,pies):
    '''
    Add new (i,j,tag) scores
    '''
    for X in pies.keys():
        scores[(i,j,X)] = pies[X][-1]
    return scores

def update_tags(i,j,tags,pies):
    '''
    Add new (i,j) --> c(tags)
    '''
    tags[(i,j)] = pies.keys()
    return tags

def update_bp(i,j,bp,pies):
    '''
    Add new backpointers to bp:
    (split point, lft,rgt)
    '''
    for X in pies.keys():
        bp[(i,j,X)] = (pies[X][0],
                       pies[X][1],
                       pies[X][2])
    return bp

