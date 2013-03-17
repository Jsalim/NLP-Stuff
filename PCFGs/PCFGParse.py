import sys, os
import nltk
from PCFG_util import makeQandRR,rebuildBest
from PCFG_util import save_model,load_model
from PCFG_util import functionizeQC
from PCFGs import CKY_alg01


class PCFGSimpleParser:

    def __init__(self, train_trees=list(),model_path=False):
        if model_path:
            self.load(model_path)
        else:
            print('Initializing parser')
            self.train(train_trees)

    def train(self,train_trees):
        '''
        Train parser using input trees, or treebank
        stuff if no trees provided.  Configure fitter
        based on q, revR obtained
        '''
        if len(train_trees)==0:
            train_trees = nltk.corpus.treebank.parsed_sents()
        self._q, self._qC, self._revR = makeQandRR(train_trees)

    def fit(self,sent):
        '''
        Given a new sentence, returns the parsing of that
        sentence using the current method implimented
        '''
        if hasattr(self,"_q") and hasattr(self,"_revR"):
            return self.fitSent(sent,
                                {'revR':self._revR,
                                 'q':self._q})
        else:
            print("No model associated with parser yet")

    
    def fitSent(self,sent,G):
        #sent = preprocessSent(sent)
        bp = CKY_alg01(sent,G)
        return rebuildBest(len(sent)-2,bp)

    def save(self,out_path):
        save_model((self._qC,self._revR),out_path)

    def load(self,in_path):
        (qC,revR) = load_model(in_path)
        self._qC = qC
        self._q = functionizeQC(qC)
        self._revR = revR
