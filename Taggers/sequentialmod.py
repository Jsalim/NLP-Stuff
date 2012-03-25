from nltk import NgramTagger
import yaml

class UniModTagger(NgramTagger):
    """
    A tagger that chooses a token's tag based the preceeding
    word's string and tag.
    Unigram taggers are typically trained on a tagged corpus.
    """
    yaml_tag = '!nltk.UniModTagger'

    def __init__(self, train=None, model=None,
                 backoff=None, cutoff=0, verbose=False):
        NgramTagger.__init__(self, 1, train, model,
                             backoff, cutoff, verbose)

    def context(self, tokens, index, history):
        if index==0:
            tag_context = tokens[0]
        else:
            tag_context = tuple(history[max(0,index-1)])
        return tag_context
