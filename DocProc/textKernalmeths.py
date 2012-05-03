import math
import random
import nltk
from nltk.corpus import brown
from nltk.corpus import stopwords
from cPickle import dump


class KernalMethsOp():
    def __init__(self, docs=None, Stops='default', lang='english'):
        if not docs:
            self._getBrownDocs(stopwords)
        else:
            self._docs = docs
            self._getInputDocs(stopwords)

    def _getInputDocs(self, Stops):
        '''
        Takes an input of docs provided by user and performs the necessary
        calcs in order to make use of them in Kernal operations.  
        '''
        stops = self._getStopwords(Stops, lang=lang)
        main_dict = nltk.defaultdict(list)
        weight_dict = nltk.defaultdict(int)
        
        # need to include various options to allow for feeding in file names
        # or actualy documents; if they are providing sets of documents per-
        # taining to particular categories, and they want these averaged to-
        # gether for comparison purposes; etc.

        self._vecs = main_dict

    def _getBrownDocs(self, Stops):
        '''
        Create reference distributions from the Brown corpus,
        seperated by cetegories.  Non=tagged data (i.e., tags are
        removed).  We assume that each category of docs is actually a single
        document of that category.  This instance is mainly for test cases,
        and likely of little use to a user, except for basic comparisons.
        Also, this really only needs to be done once (unless stopwords are
        changed), since we can just pickle it and re-use it later.
        '''
        stops = self._getStopwords(Stops, lang=lang)
        main_dict = nltk.defaultdict(list)
        weight_dict = nltk.defaultdict(int)
        # first, load the files from brown topics (minus the two small ones)
        for category in set(brown.categories()).\
            difference(set(['humor', 'science_fiction'])):
            cat_files = brown.fileids(categories=category)
            key_list = []           # misleading; list of words encountered
            temp_weight_dict = nltk.defaultdict(int)
            for f in cat_files:
                temp = brown.open(f).read().split()
                # brown files are tagged, so get rid of that info, for now
                temp = [entry.split('/')[0] for entry in temp]
                temp = [entry for entry in temp if entry not in stops]
                main_dict[category].append(self._FDtoDIC(nltk.FreqDist(temp)))
                # update the weight dict for this category
                temp_weight_dict['__NUM__'] += 1
                for entry in main_dict[category][-1].keys():
                    temp_weight_dict[entry] += 1
                key_list.extend(main_dict[category][-1].keys())
                key_list = set(key_list)
                cat_avg_dict = {}
                for word in key_list:
                    score = 0.0
                    for fdd in main_dict[category]:
                        score += float(fdd[word])/fdd['N']
                    cat_avg_dict[word] = float(score) / \
                                         len(main_dict[category].keys())
                main_dict[category].append(cat_avg_dict)
            # get weights for current category
            self._R_[category] = self._calcWeights(temp_weight_dict)
            # update the main weight dict for all docs
            for key in temp_weight_dict.keys():
                weight_dict[key] += temp_weight_dict[key]
            self._R_['__ALL__'] = self._calcWeights(weight_dict)
            ## need to add this...
            main_dict['__ALL__'] = ...
        self._vecs = main_dict

    def _calcWeights(self, usage_dict, mode=0):
        '''
        This calculates the default R weighting matrix (diag) for the words
        in the various documents and categories.  If categories are provided,
        an R matrix is calculated for each separate category, and an overall
        R matrix is calculated for the entire document data set. The R
        "matrix" is actually returned as a dictionary of word:weight pairs.
        Calculation from "Text Mining" pp.14 [1] used. >w(t) = ln(l/df(t))<
        Can add other weighting formulas if desired.
        '''
        R_ = {}
        if mode==0:         # default weighting
            num_docs = usage_dict.pop('__NUM__')
            for key in usage_dict.keys():
                R_[key] = math.log(float(num_docs) / usage_dict[key], math.e)
        return R_

    def _calcProxMat(self, mode=0):
        '''
        This calculates the proximity matrix for the document set in
        self._vecs. Returns PP', not P (or function to calc on the fly).
        In the simple case, the matrix is symmetric, so only returns
        scores for (w1, w2) -or- (w2, w1).
        '''
        P_ = {}
        if mode==0:         # default prox; D'
            doc_names = self._vecs.keys()
            try: doc_names.remove('__ALL__')
            except ValueError: pass
            for i, w1 in enumerate(self._weights['__ALL__'].keys()):
                score = 0.0
                for j, w2 in enumerate(self._weights['__ALL__'].keys()[i+1:]):
                    for vec in doc_names:
                        score += self._vecs[vec][w1]*self._vecs[vec][w2]
                # should check to make sure above some min value,
                # to preserve space, etc.  If not above min, don't
                # give entry; just assume 0 when checking
                P_[w1, w2] = score

        return P_
                    

    def _FDtoDIC(self, fd):
        '''
        As it turns out, nltk Frequency Distributions are not compatable w/
        pickling.  So, this function rips out the desired props from a 
        FreqDist (i.e., length and word:freq pairs) and places them in a
        regular dictionary that can be pickled.
        '''
        out_dict = nltk.defaultdict(float)
        for key in fd.keys():
            out_dict[key] = fd[key]
        out_dict['N'] = fd.N()
        return out_dict


    def _getStopwords(self, Stops, lang='english'):
        '''
        Handles stopwords.  If 'default', just sets stops to nltk default
        stopwords.  If a list, assume that user is supplying a list of
        stopwords to use.  If the list provided ends in 'nltk.default',
        the nltk stopwords are appended to the list.  If set as 'None',
        then no stopwords are used (i.e., stops = [])
        '''
        if type(Stops)==list:
            stops = Stops
            if stops[-1]=='nltk.default':
                stops = stops[:-1].append(stopwords.words(lang))
        elif Stops == None:
            stops = []
        else:
            stops = stopwords.words(lang)
        return stops

    def _getText(self, i, doc, TorF):
        '''
        General function for retreiving set of names, texts handed
        as arguments by user.  Used in both __init__ phase when
        user specifies documents to use as main Kernal vecs, and when
        user is comparing documents to the main Kernal vecs.
        '''
        if type(TorF)==list:
            name, text = self._getText(0, doc, TorF[i])
        elif TorF=='File':
            name, text = self._getFileText(doc)
        elif TorF=='Text':
            try:
                name, text = doc.name, doc.text
            except AttributeError:
                name, text = "Doc"+str(i), doc
        return name, text
        
    def _getFileText(self, path):
        '''
        If file name given as a document, retrieve the text from that
        file and the name of the file, and return these elements.  If
        the path given is not a file, notify and return a default
        'no name' and empty text list.
        '''
        if os.path.isfile(doc):
            name = os.path.basename(doc).split('.')[0]
            with open(doc, 'r') as f1:
                raw = f1.read()
            return name, raw
        else:
            print "Doc " + str(doc) " does not exist."
            return '****', []

    def _calcScore(self, fdd, name):
        '''
        Given a freq distribution (dictionary) corresponding to the document
        one wishes to analyze, calculates the inner product of it and the
        default set of documents stored in self._vecs.  Terms found in the
        test document, but not in the self._vecs documents are ignored. The
        fraction of such terms, relative to the test doc, is returned.
        '''
        score = 0.0
        count = 0
        comp = self._vecs[name]
        for word in fdd.keys():
            try:
                score += float(fdd[word]) * \
                         float(comp[word])
                count += 1
            except KeyError: pass
        score /= len(fdd.keys()) / float(count)
        return score, 1.0 - float(count) / len(fdd.keys())

    def compKernal(self, docs, cat='__ALL__', TorF='Text'):
        sim_scores = {}
        for i, doc in enumerate(docs):
            name, text = self._getText(i, doc, TorF)
            if text != []:
                fdd = self._FDtoDIC(nltk.FreqDist(text))
                sim_scores[name] = nltk.defaultdict(float)
                if cat=='ALL*': cat = self._vecs.keys()
                for c in cat:
                    sim_scores[name][c], miss_frac = self._calcScore(fdd,c)
            


                
        
                                            
