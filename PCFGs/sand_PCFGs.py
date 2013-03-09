import nltk
from collections import defaultdict

def PCFG_training(training_data):

    #Construct, for each word, list of possible POS tags,
    #as observed in G[R]
    words = unique(sent)
    end_PIs = dict()
    for w in words:
        end_PIs[w] = blah
        return
    #Now, assuming we have a real training set, for each Phrase
    #tag, count the number of time it splits into other pairs
    #of Phrase/POS tags; this will be used in the calculation
    #of q(X --> YZ).  This should really be something handed
    #to this part of the code by a training process...
    tags = unique() 

def CKY_alg(sent,G):
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
        (e.g., q(a) = count(a -> b)/count(a))
    returns the maximum liklihood parsing...

    'sent' is just a list of words
    '''
    revR = G['revR']
    q = G['q']

    tags,scores,bp = intialize_Refs(sent,revR,q)
    '''This determines '''
    for l in range(0,len(sent)-1):
        '''This determines the starting point of the subsentence'''
        for i in range(0,len(sent)-l):
            '''This determines the '''
            j = l+i
            #This is the part where we take each of the current
            #level tags and attempt to merge into higher-level
            #tags
            tags,scores,bp = CKY_meat(revR,q,
                                      i,j,
                                      tags,scores,bp)
    '''Retreive the MLE solution'''
    out = rebuildBest(scores,bp)

def CKY_meat(revR,q,i,j,tags,scores,bp):
    '''
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
                Xs = revR[(l,r)]
                #Need corresponding probability of each Y,Z
                for x in Xs:
                    temp_pies[x].append(s,l,r,
                                        q[(x,l,r)]*yProb*zProb)

    #Update everything and spit back out
    return update_refs(i,j,temp_pies,scores,tags,bp)

def initialize_Refs(sent,revR,q):
    '''Populate bp and scores  with words from the sentence'''
    tags = initialize_tags(sent,revR)
    scores = initialize_scores(sent,q)
    bp = intialize_bp(sent,tags)
    return scores,tags,bp
    
def initialize_scores(sent,q,tags):
    '''
    Initialices the scores dictionary with an entry
    for each (i,i,POS) tuple, i.e., create an entry
    for every POS tag associated with each word as
    the probability of that word having that POS
    '''
    scores = dict()
    for i,w in enumerate(sent):
        for POS in tags[(i,i,w)]:
            #Set 'r' to '-1' in q for single words
            scores[(i,i,POS)] = q[(POS,w,-1)]
    return scores

def initialize_tags(sent,revR):
    '''
    Initialise 'tags' with the list of observed
    POS tags for each word in the sentence.
    '''
    tags = dict()
    for i,w in enumerate(sent):
        tags[(i,i,w)] = revR[w]
    return tags

def initialize_bp(sent,tags):
    '''
    Initializes bp with the words in sentence;
    makes an entry for each (word,POS) combo
    '''
    bp = dict()
    for i,w in enumerate(sent):
        for t in tags[(i,i)]
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
    Add new backpointers to bp
    '''
    for X in pies.keys():
        bp[(i,j,X)] = (pies[X][0],
                       pies[X][1],
                       pies[X][2])
    return bp

def rebuildBest(n,bp):
    '''
    Rebuilds the best parse tree from the 'scores'
    and 'bp' dictionaries, which are the (i,j,X)
    probabilities and (i,j,X) (s,Y,Z) tuples,
    respectively
    '''
    start = bp[(0,n,'S')]   #This is the prob of the sentence
    levels = recurDig(bp,0,start[0],n,start[1],start[2])
    return levels

def recurDig(bp,i,s,j,Y,Z):
    '''
    Recursively get the lft and rgt branches of each
    split down teh parse tree.  Encountering i==j (i.e.,
    start index equals stop index) bottoms out the tree
    and returns the word at position i (j) in the
    sentence along with its best tag.
    '''
    if i==j:    #So s==i for word-level combos
        return (Y,bp[(i,j,Y)])
    else:
        lft_d = bp[(i,s,Y)]
        lft = recurDig(bp,i,lft_d[0],s,lft_d[1],lft_d[2])
        rgt_d = bp[(s+1,j,Z)]
        rgt = recurDig(bp,s+1,rgt_d[0],j,rgt_d[1],rgt_d[2])
        return (lft,rgt)
    
        
        
