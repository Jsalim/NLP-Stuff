import nltk
from nltk import NgramTagger
import yaml
from random import random

class StatTagger(NgramTagger):
    """
    A tagger that uses basic statistical FreqDist methods to determine
    most likely tag in a context not seen in the training data.  Tagger
    uses proceeding n-1 POS tags to determine most likely current word
    tag.
    """

##    yaml_tag = '!nltk.StatTagger'
    
    def __init__(self, train=None, model=None,
                 backoff=None, cutoff=0, n = 2, verbose=False):
        self._method = 'Lidstone'
        self._gamma = 1
        self._n = n
        self._bins = None
        self._backoff = backoff
        NgramTagger.__init__(self, self._n, train, model,
                             backoff, cutoff, verbose)

    def _train(self, tagged_corpus, cutoff=0, verbose=False):
        self._primary = nltk.UnigramTagger(tagged_corpus)
##        self._primary = nltk.NgramTagger(self._n, tagged_corpus, \
##                                         backoff=self._backoff)
        self._context_to_tag = self.getLookup(tagged_corpus)

    def choose_tag(self, tokens, index, history):
        """
        This choose_tag is essentually the same as that of the ContextTagger
        class, except that it deals with instances where multiple, equally
        probable tags exist for a given context.  This is more likely than
        would seem, since probabilities of similar value are treated as equal.
        """
        if self._n-1 > index:
            temp = self._primary.choose_tag(tokens, index, history)
        else:
            pri = self._primary.choose_tag(tokens, index, history)
            if pri==None:
                context = self.context(tokens, index, history)
                sec = self._context_to_tag.get(context)
                if sec:
                    temp = sec[int(len(sec) * round(random(), 5) - .00001)]
                else:
                    #temp = self._mostfreq
                    temp = 'NN'
            else:
                temp = pri
        return temp

    def context(self, tokens, index, history):
        tag_context = tuple(history[(index-self._n+1):index])
        return tag_context

    def getNGramTagFD(self, tagged_corpus):
        fd_ngram = nltk.FreqDist()
        for sentence in tagged_corpus:
            ngrams = nltk.ngrams((tag for (word, tag) in sentence), self._n)
            for context in ngrams:
                fd_ngram[context] += 1
        return fd_ngram

    def getLidstoneTag(self, tagged_corpus):
        """
        Converts the provided frequency distribution into a Lidstone estimation
        using the nltk.probability module.  Gamma=1, bins=None is Laplace.
        This estimation is used to decide which tag to assign given the tag-
        context observed in the test tagged corpus. Creates necessary fd from
        training tagged corpus.
        """
        fd = self.getNGramTagFD(tagged_corpus)
        td_ngram = nltk.LidstoneProbDist(fd, self._gamma, bins=self._bins)
        return td_ngram

    def getInstances(self, tagged_corpus):
        """
        Obtains the set of all ngram tag sequences found in the sentences
        of the tagged corpus provided as training data.
        """
        ngram_types = []
        for sentence in tagged_corpus:
            ngrams = nltk.ngrams((tag for (word, tag) in sentence), self._n)
            for context in set(ngrams):
                ngram_types.append(context)
        ngram_types = set(ngram_types)
        return ngram_types

    def getInstDict(self, tagged_corpus):
        """
        Creates a look-up dictionary with (n-1)gram tag sequence keys that returns
        a list of n-th position tags observed for ngram tag sequences in the
        training tagged corpus.
        """
        instDict = nltk.defaultdict(list)
        ngram_types = self.getInstances(tagged_corpus)
        for entry in ngram_types:
            instDict[tuple(list(entry)[:self._n-1])].append(entry)
        return instDict

    def getProbDict(self, td, tagged_corpus):
        """
        Using the Lindstone est., create dict of lists of (tag, prob) tuples
        for the observed (n-1)grams. 'Tag' here is a member of an (n-1)gram's
        corresponding set of observed n-th gram tags, and 'prob' is the
        associated probabilty of observing the entire ngram tag sequence
        in the tagged corpus training set.
        """
        instDict = self.getInstDict(tagged_corpus)
        instProbDict = nltk.defaultdict(list)
        for key in instDict.keys():
            for tag in instDict[key]:
                instProbDict[key].append((list(tag)[-1],td.prob(tag)))
        return instProbDict

    def trimedProbDict(self, td, tagged_corpus):
        """
        Modifies the probabilty dictionary obtained by removing all but the
        maximum probability entry(ies).  If ties exist, they are saved, and
        one is randomly chosen if the context is encountered in the test set.
        The reasoning behind this, I think is clear.  Differing to a default
        backoff tagger is another option, though it would seem that assigning
        a random, known-high-robability tag is better than assigning a default.
        """
        instProbDict = self.getProbDict(td, tagged_corpus)
        for key in instProbDict.keys():
            temp  = instProbDict[key]
            max_prob = max(prob for (tag, prob) in temp)
            temp = [tag for (tag, prob) in temp if prob>=max_prob]
            instProbDict[key] = temp
        return instProbDict

    def getLookup(self, tagged_corpus):
        td = self.getLidstoneTag(tagged_corpus)
        self._mostfreq = td.max()
        lookupDict = self.trimedProbDict(td, tagged_corpus)
        return lookupDict


    
