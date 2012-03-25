'''
The goal of this is to determine the set of words used in defining other words
in the dictionary, so that a directed graph can be constructed with edges pointing
from a particular word to other words that are contained within its definition,
where edges are weighted by the frequency a particular word occurs in another's
definitions;
'''

import sys, os
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from cPickle import dump

def DFDtoDICT(default_dict):
    def_map = {}
    for key in definition_relations.keys():
        temp = []
        for word in definition_relations[key].keys():
            temp.append((word, definition_relations[key][word],))
        def_map[key] = temp
    return def_map

try:
    mode = sys.argv[1]
except:
    mode = '0'
print mode

if mode=='0':
    '''
    Attempt Num 1:  Works O.K., but only grabs existing synsets.  Therefore,
    if a word is not at the head of a synset (e.g., 'perhaps'), then the
    word is never added to the list, even though wn recognizes the word
    and directs it to a synset (in this case, 'possibly.r.01').  Need to
    iterate over some list of words to get a full map, though could potentially
    just grab the items unique to a complete list, and see what the head
    word of their default synset is...
    '''
    definition_relations = nltk.defaultdict(lambda: nltk.defaultdict(int))
    stops = stopwords.words('english')
    punct = ["`", "'", '"', '.', ',', ':', ';', \
             '/', '~', '(', ')', '{', '}', '[', ']']
    stops.extend(punct)

    # iterate over synsets, grab names and words from defs
    for syn in wn.all_synsets():
        name = syn.name.split('.')[0]
        for word in nltk.word_tokenize(syn.definition):
            if word.lower() not in stops and word.lower != name:
                definition_relations[name][word.lower()] += 1

    # convert to reg dic
    def_map = DFDtoDICT(definition_relations)
            
    # dump to pickle
    with open('def_mapping01.pkl', 'wb') as f:
        dump(def_map, f, -1)

elif mode=='1':
    '''
    Attempt Num 2: Same as above, only iterating over lemma-words instead of
    all synsets...
    This seems to be fairly successful :)
    '''
    definition_relations = nltk.defaultdict(lambda: nltk.defaultdict(int))
    stops = stopwords.words('english')
    punct = ["`", "'", '"', '.', ',', ':', ';', \
             '/', '~', '(', ')', '{', '}', '[', ']']
    stops.extend(punct)
    for name in wn.all_lemma_names():
        synsets = wn.synsets(name)
        for syn in synsets:
            word = syn.name.split('.')[0]
            for w in nltk.word_tokenize(syn.definition):
                if w.lower() not in stops and w.lower != name:
                    definition_relations[name][w.lower()] += 1
            if word != name:
                definition_relations[name][word.lower()] += 5

    # convert to reg dic
    def_map = DFDtoDICT(definition_relations)

    # dump to pickle
    with open('def_mapping02.pkl', 'wb') as f:
        dump(def_map, f, -1)


    
##--------------------------------------------------
##synsets = wn.synsets(word)
##for syn in synsets:
##    print "Name:", synset.name
##    print "Lexical Type:", synset.lexname
##    print "Lemmas:", synset.lemma_names
##    print "Definition:", synset.definition
##    for example in synset.examples:
##        print "Example:", example
##--------------------------------------------------
