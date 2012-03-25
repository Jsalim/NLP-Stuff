import os, sys, nltk
import textprocesses
from nltk.corpus import brown


def getSimWordNet(word, text=None, num_word=40, num=5):
    """
    This function uses the nltk.similar(word) function to create a dictionary
    with keys being the top "num_word" words in nltk.similar("word").  Entries
    are a list of tuples consisting of the top "num" word for nltk.similar(word)
    for each key and the corresponding inverse ranking (1/1, 1/2, ..., 1/num)
    of the word in the nltk.similar(key) list.  Instances of "word" in any of
    these lists are ignored.
    """
    text = text if text else nltk.Text(brown.words())
    text = textprocesses.TextProcess(text)
    num += 1                            # accounts for pos of 'word' in sim
    simWords = text.getsimilar(word, num_word)
    simWords = removePunc(simWords)     # need to make this mod
    wordNetDict = nltk.defaultdict(list)
    for w in simWords:
        wSim = text.getsimilar(w, num)
        # remove word from sim. list if present
        try:
            wSim.remove(word)
        except: pass
        # create entry for w using the first num words in wSim
        for s in wSim[:num-1]:
            wordNetDict[w].append((s,1.0/num))
    return wordNetDict

def removePunc(words):
    """
    Gets rid of punctuation in the original nltk.similar("word") list..
    """
    punc_list = ['.', "'", '"', "`", "``", "?", "!", "@", ",", "..."]
    temp_out = []
    for word in words:
        if word not in punc_list:
            temp_out.append(word)
    return temp_out

def dict2adjmat01(edgeWeightDict, directed=False):
    """
    This code simply takes a dictionary of the form
    dict[node00]=[(node01, edge0001),(node02, edge0002),...,(nodeNN, edge00NN)]
    and transforms it into an adj "matrix"/list of the form
    [(node00,node01,edge0011), node(00,node02,edge0002),...].
    Converts to a symetric adj. "matrix" unless directed is set to "True".
    """
    adjMat = []
    for key in edgeWeightDict.keys():
        for (node, edge) in edgeWeightDict[key]:
            adjMat.append((key,node,edge))
            adjMat.append((node,key,edge))
    adjMat = list(set(adjMat))
