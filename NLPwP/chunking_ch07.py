import sys, os, nltk
from nltk.corpus import conll2000       # WSJ tagged shit

'''
NP Chunking using grammars
'''
sentence = 'the little yellow dog barked at the cat.'
sentence = nltk.word_tokenize(sentence)
sentence = nltk.pos_tag(sentence)
sentence[2] = ('yellow', 'JJ')
grammar = "NP: {<DT>?<JJ>*<NN>}"
cp = nltk.RegexpParser(grammar)
result = cp.parse(sentence)
result.draw()       # starts sep window with pic..oooooo

# above is a weak grmmer; try:
grammar = "NP: {<DT>?<JJ.*>*<NN.*>+}"
cp = nltk.RegexpParser(grammar)
# etc...

# using reg expressions:
grammar = r"""
    NP: {<DT|PP\$>?<JJ.*>*<NN>} # chunk determiner/possesive, adjectives, and nouns
        {<NNP>+}                # chunk sequences of proper nouns
"""
cp = nltk.RegexpParser(grammar)
sentence = "Rapunzel let down her long golden hair."
sentence = nltk.word_tokenize(sentence)
sentence = nltk.pos_tag(sentence)
sentence[5] = ('golden', 'JJ')  # broke again
sentence[3] = ('her', 'PP$')
print cp.parse(sentence)
