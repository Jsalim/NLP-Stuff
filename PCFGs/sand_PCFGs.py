import nltk


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
    #Construct, for each word, list of possible POS tags,
    #as observed in G[R]
    words = unique(sent)
    end_PIs = dict()
    for w in words:
        end_PIs[w] = blah

    for i in range(0,len(sent)-1):
        for j in range(0,len(sent)-i):
            k = i+j
