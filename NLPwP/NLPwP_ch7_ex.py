import os, sys, nltk

# from pp 268; modulizing of chunk-finder code; accepts arb CHUNK,
# returns matches found in brown, or whatever corpus handed to it
def find_chunks(CHUNK, docs=None):
    cp = nltk.RegexpParser(CHUNK)
    key_term = CHUNK.split(':')[0]
    docs = docs if docs else ntlk.corpus.brown
    try:
        temp = docs.__getattribute__('tagged_sents')
        found_matches = []
        for sent in docs.tagged_sents():
            tree = cp.parse(sent)
            for subtree in tree.subtrees():
                if subtree.node==key_term:
                    found_matches.append(subtree)
        return found_matches
    except ValueError:
        print 'No tagged sentences attribute in docs.'
        
