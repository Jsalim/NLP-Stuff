#Basic import stuff for running 
import re, nltk, os
from urllib import urlopen
#Article from HBR
url = "http://hbr.org/2011/12/first-lets-fire-all-the-managers/ar/1?referral=00134"
#Get it
raw = urlopen(url).read()
#Clean it
raw = nltk.clean_html(raw)
#Cut it
sentences = nltk.sent_tokenize(raw)
#Cut it again
sentences = [nltk.word_tokenize(sent) \
            for sent in sentences]
#Label it
sentences = [nltk.pos_tag(sent) \
             for sent in sentences]
#Ch. 7 Chunking Stuff; NP
NPgrammar = "NP: {<DT>?<JJ>*<NN>}"
cp = nltk.RegexpParser(NPgrammar)
NPresults = [cp.parse(sent) \
             for sent in sentences]
NPgrammar_mod01 = "NP: {<DT>?<JJ.*>*<NN.*>+}"
cp = nltk.RegexpParser(NPgrammar_mod)
NPresults_mod = [cp.parse(sent) \
             for sent in sentences]
#And another (mine)
NPgrammar_mod02 = '''NP: {<DT>?<JJ.*>*
(<JJ.*>|<IN.*>|<VB(G)?>|<CD.*>)*
(<NN.*><IN.*>)?<NN.*>+}'''
#And another...
NPgrammar_mod03 = '''NP: {(<DT>?|<PRP.*>)
(<JJ.*>(<IN.*>)?|<VBG>(<IN.*>)?|(<\$>?<CD.*>(\,<CD.*>)?)(<IN.*>)?)*
((<NN.*>+|<\$>?<CD.*>)<IN.*>)?(<NN.*>+|<\$>?<CD.*>)}'''
