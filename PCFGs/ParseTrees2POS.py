import nltk
from collections import defaultdict

def simp_tag(tag):
    '''Simplifies tags to brown-style'''
    return nltk.tag.simplify_brown_tag(tag)

def walk_sent_trees(sents,simple=True):
    '''
    Walks the sentence tree
    '''
    tree_list = list()
    for sent in sents:
        sent.chomsky_normal_form()
        tree_list.extend(recur_walk(sent,simple))
        else:
    return tree_list

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
        tree_list.extend(recur_walk(tree[0]))
    if len(tree[1])>1:
        #Ditto, but for rgt
        tree_list.extend(recur_walk(tree[1]))
    return tree_list


