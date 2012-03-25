'''
Meant to be ch6 q8 response; for low-freq words that may be
important to determining nature of content, but may not appear
in the training set at all or enough, need a tool for obtaining
more frequent words with the same meaning; need to get context,
POS of word in question in order to accurately use Wordnet to
obtain a set of similar words.
'''

import nltk
from nltk.corpus import wordnet as wn

synsets = wn.synsets(word)
keep = []
# only keep those with same pos as word
for syn in synsets:
    if syn.name.split('.')[1] == word_pos:
        keep.append(syn)
 
