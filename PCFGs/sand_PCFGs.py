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
    q   --> MLE from training (e.g., q(a) = count(a -> b)/count(a))
    returns the maximum liklihood parsing...
    '''
    

    '''This determines '''
    for l in range(0,len(sent)-1):
        '''This determines the starting point of the subsentence'''
        for i in range(0,len(sent)-l):
            '''This determines the '''
            j = l+i
            #This is the part where we take each of the current
            #level tags and attempt to merge into higher-level
            #tags
            tags,scores = CKY_meat(i,j,tags,revR,q,scores)

def CKY_meat(i,j,tags,revR,q,scores):
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
                    temp[x].append(s,l,r,
                                   q[x,l,r]*yProb*zProb)
    #Update everything and spit back out
    temp_pies = clean_pies
    scores = update_scores(scores,temp_pies)
    tags = update_tags(tags,temp_pies)
    return tags,scores

def clean_pies(temp_pies):
    '''
    Find best X --> YZ transition for each X occuring
    in the temp_pies
    '''
    return pies

def update_scores(scores,pies):
    '''
    Add new (i,j,tag) scores
    '''
    return scores

def update_tags(tags,pies):
    '''
    Add new (i,j) --> c(tags)
    '''
    return tags

        
        
