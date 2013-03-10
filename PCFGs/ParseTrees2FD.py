import nltk
from collections import defaultdict
from PCFG_util import simp_tag

def getSentTreeFD(sents,simple=True):
    '''
    Walks the sentence trees
    '''
    tree_list = list()
    for sent in sents:
        sent.chomsky_normal_form()
        tree_list.extend(recur_walk(sent,simple))
    treeFD = nltk.FD(tree_list)
    return treeFD

def recur_walk(tree,simple):
    '''
    Given a sentence parsing tree, recursively
    walks the tree and returns a list of
    X -> YZ split pairs, assuming the tree
    is in Chomsky-normal form. Returns list of
    tuples: (X,Y,Z) where X is the node tag,
    Y is the left branch tag, and Z is the
    right branch tag.
    '''
    tree_list = list()
    #Grab the current
    if simple:
        tree_list.append((simp_tag(tree.node),
                          simp_tag(tree[0].node),
                          simp_tag(tree[1].node)))
    else:
       tree_list.append((tree.node,
                         tree[0].node,
                         tree[1].node))
    if len(tree[0])>1:
        #Traverse the lft branch if not a word
        tree_list.extend(recur_walk(tree[0],simple))
    if len(tree[1])>1:
        #Ditto, but for rgt
        tree_list.extend(recur_walk(tree[1],simple))
    return tree_list
