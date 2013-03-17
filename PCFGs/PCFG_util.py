import sys, os
import nltk
from collections import defaultdict
import pickle


def simp_tag(tag):
    '''Simplifies tags to brown-style'''
    return nltk.tag.simplify_brown_tag(tag)

def getRefs(source='treebank',size=500):

    trees = getTrees(source,size)
##    q, revR = makeQandRR(trees)
    return makeQandRR(trees)

def makeQandRR(trees):

    '''Make FDs for POS-Word pairs and POS-SentPart pairs'''
    WordPOSFD = getWordPOSFD(trees) #From wordPOS2FD
    SentPOSFD = getSentPOSFD(trees) #From ParseTrees2FD
    q,qC = makeQ(SentPOSFD,WordPOSFD)
    revR = makeRR(SentPOSFD,WordPOSFD)
    return q, qC, revR

def getTrees(source,size):
    '''Load the trees from source, return first SIZE trees'''
    if source=='treebank':
        from nltk.corpus import treebank
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
    return functionizeQC(q), q

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

def functionizeQC(qC):
    '''
    float(qC[('NP','NP','NP')])/qC[("NP",'*','*')]
    float(qc[('ADJ','simple')]/qC[('w','ADJ')]
    '''
    def q(x):
        if len(x)==2:
            return float(qC[x]) / qC[('w',x[0])]
        elif len(x)==3:
            return float(qC[x]) / qC[(x[0],'*','*')]
    return q

def PCFG_training01(training_trees=list()):
    '''
    Simple training using either parsed trees provided
    by user, or treebank if no trees provided.  Returns
    q and revR generated from the training data.
    '''
    if len(training_trees)==0:
        qC,revR = getRefs()
    else:
        qC,revR = makeQandRR(training_trees)
    q = functionizeQC(qC)
    return q,revR

def getWordPOSFD(trees,simple=True):
    '''
    For all sents in the doc, count the number of times
    each POS-word combo appears in the doc.
    '''
    wPOS_list = list()
    for sent in trees:
        wPOS_list.extend(word_POS_grab_sent(sent,simple))
    wPOSFD = nltk.FreqDist(wPOS_list)
    return wPOSFD

def word_POS_grab_sent(sent,simple):
    '''
    Iterate over items at height 2 in sent tree
    and count number of times each POS-word combo
    appears.  Keys are (POS, word) tuples.  Also,
    nest POS appearences within lost; preface all
    word POS tags with 'w' (so tuple should be
    ('w',POS).
    '''
    if simple:
        wPOSlist = [(simp_tag(s.node),s[0]) for s in \
                    sent.subtrees(lambda t: t.height() == 2)]
        wPOSlist.extend([('w',simp_tag(s.node)) for s in\
                         sent.subtrees(lambda t: t.height() == 2)])
    else:
       wPOSlist = [(simp_tag(s.node),s[0]) for s in \
                   sent.subtrees(lambda t: t.height() == 2)]
       wPOSlist.extend([('w',s.node) for s in\
                        sent.subtrees(lambda t: t.height() == 2)])
    return wPOSlist

def getSentPOSFD(sents,simple=True):
    '''
    Walks the sentence trees
    '''
    tree_list = list()
    for sent in sents:
        if len(sent)>2:
            sent.chomsky_normal_form()
            tree_list.extend(recur_walk(sent,simple))
    treeFD = nltk.FreqDist(tree_list)
    return treeFD

def recur_walk(tree,simple):
    '''
    Given a sentence parsing tree, recursively
    walks the tree and returns a list of
    X -> YZ split pairs, assuming the tree
    is in Chomsky-normal form. Returns list of
    tuples: (X,Y,Z) where X is the node tag,
    Y is the left branch tag, and Z is the
    right branch tag.  Also count occurances of
    X --> (X, '*', '*') tuples.  We don't double-count
    word POS tags here, because we only add (X,*,*) if
    X has non-word children.
    '''
    tree_list = list()
    #Grab the current
    if simple:
        tree_list.append((simp_tag(tree.node),
                          simp_tag(tree[0].node),
                          simp_tag(tree[1].node)))
        tree_list.append((simp_tag(tree.node),'*','*'))
    else:
       tree_list.append((tree.node,
                         tree[0].node,
                         tree[1].node))
       tree_list.append((tree.node,'*','*'))
    if len(tree[0])>1:
        #Traverse the lft branch if not a word
        tree_list.extend(recur_walk(tree[0],simple))
    if len(tree[1])>1:
        #Ditto, but for rgt
        tree_list.extend(recur_walk(tree[1],simple))
    return tree_list

def rebuildBest(n,bp,method='simple'):
    if method=='simple':
        return rebuildBest01(n,bp)
    elif method=='lexical':
        return rebuildBest02(n,bp)

def rebuildBest01(n,bp):
    '''
    Rebuilds the best parse tree from the 'scores'
    and 'bp' dictionaries, which are the (i,j,X)
    probabilities and (i,j,X) (s,Y,Z) tuples,
    respectively
    '''
    if (0,n,'S') in bp.keys():
        start = bp[(0,n,'S')]   #This is the prob of the sentence
    elif (0,n,'S|<S') in bp.keys():
        start = bp[(0,n,'S|<S')]
    levels = recurDig01(bp,0,start[0],n,start[1],start[2])
    return levels

def recurDig01(bp,i,s,j,Y,Z):
    '''
    Recursively get the lft and rgt branches of each
    split down the parse tree.  Encountering i==j (i.e.,
    start index equals stop index) bottoms out the tree
    and returns the word at position i (j) in the
    sentence along with its best tag.
    '''
    lft_d = bp[(i,s,Y)]
    if i < s:
        lft = (Y, recurDig01(bp,i,lft_d[0],s,lft_d[1],lft_d[2]))
    else:
        lft = (Y,lft_d)
    rgt_d = bp[(s+1,j,Z)]
    if s+1 < j:
        rgt = (Z, recurDig01(bp,s+1,rgt_d[0],j,rgt_d[1],rgt_d[2]))
    else:
        rgt = (Z,rgt_d)
    return (lft,rgt)

def save_model(model,out_path):
    #out_path = get_paths()["model_path"]
    pickle.dump(model, open(out_path, "w"))

def load_model(in_path):
    #in_path = get_paths()["model_path"]
    return pickle.load(open(in_path))
