import sys, os, nltk
from nltk.corpus import brown
import random

def handlecrapstr(func):
    try:
        temp = open('temp.txt', 'w')
        sys.stdout = temp
        exec func
        temp.close()
    finally:
        sys.stdout = sys.__stdout__
        temp.close()
        os.remove('temp.txt')

def nMostFreq(N, words):
    wCounts = nltk.defaultdict(int)
    nCounts = nltk.defaultdict(int)
    for word in words:
        wCounts[word.lower()] += 1
    for key in wCounts.keys():
        nCounts[wCounts[key]] += 1
    tot = 0
    numStop = []
    while tot<N:
        numStop.append(max(nCounts.keys()))
        tot += nCounts.pop(max(nCounts.keys()))
    revWCounts = getReverseDict(wCounts)
    wordsN = []
    for num in numStop:
        wordsN.extend(revWCount[num])

def getTagsPerWord(tagged=[], wordTags=None, opts=0):
    wordTags = wordTags if wordTags else getWordTagTypes(tagged)
    tagCounts = nltk.defaultdict(int)
    for key in wordTags.keys():
        tagCounts[key] = len(wordTags[key])
    if not opts:
        return tagCounts
    else:
        return wordCounts, tagCounts
    

def getWordTagTypes(tagged):
    wordTags = nltk.defaultdict(set)
    if type(tagged[0])==list:
        for sent in tagged:
            for (word, tag) in sent:
                wordTags[word.lower()].add(tag)
    elif type(tagged[0])==tuple:
        for (word, tag) in tagged:
            wordTags[word.lower()].add(tag)
    return wordTags

    
def getSentsWTaggedWords(tagged_sents, tar_tagged_words, N=1):
    output_list = []
    for tagged_word in tar_tagged_words:
        output_list.extend([(tagged_word, s) for s in\
                        getSentsWTaggedWord(tagged_sents, tagged_word, N)])
    return output_list

def getSentsWTaggedWord(tagged_sents, tar_tagged_word, n=2):
    output_list = []
    for sent in tagged_sents:
        if tar_tagged_word in sent:
            output_list.append(sent)
    output_list = [' '.join(['/'.join(word) for word in sent])\
                   for sent in output_list]
    if n=='All':
        return output_list
    else:
        return random.sample(output_list, min(n, len(output_list)))

def getReverseDict(inDict):
    outDict = nltk.defaultdict(list)
    for key in inDict.keys():
        outDict[inDict[key]].append(key)
    return outDict
##    for entry in inDict[key]:
##        outDict[entry]=key


# get brown_tagged, sentence form
brown_tagged_s = brown.tagged_sents()
# word form:
##brown_tagged_w = brown.tagged_words()

# get all tags used in brown tagging
b_tags = sorted(set(entry[1] for entry in brown.tagged_words()))

# build a freq dist the long way (but I alread have tags...)
tag_count = nltk.defaultdict(int)
handlecrapstr('for entry in b_tags: tag_count[entry]')
for sent in brown_tagged:
    for (w, t) in sent:
        tag_count[t] += 1
# the short way...
tag_fd = nltk.FreqDist(entry[1] for sent in brown_tagged for entry in sent)

# noun stuff, q15
noun_pattern = re.compile(r'NN(/$)?(-.*)?$')
nouns_pattern = re.compile(r'NNS(/$)?(-.*)?$')
noun_all = [entry[0] for sent in brown_tagged for\
        entry in sent if noun_pattern.match(entry[1])]
nouns_all = [entry[0] for sent in brown_tagged for\
        entry in sent if nouns_pattern.match(entry[1])]
# long way...
noun = list(sorted(set(noun)))
nouns = list(sorted(set(nouns)))
noun = [n.lower() for n in noun]
nouns = [n.lower() for n in nouns]
n_count = nltk.defaultdict(int)
ns_count = nltk.defaultdict(int)
handlecrapstr('for n in noun: n_count[n]')
handlecrapstr('for n in nouns: ns_count[n]')
for n in noun:
    n_count[n.lower()] += 1
for n in nouns:
    ns_count[n.lower()] += 1
### short way
##n_fd = nltk.FreqDist(noun_all)
##ns_fd = nltk.FreqDist(nouns_all)
# still need to match up pl w/ sing...
ns_n_dict = nltk.defaultdict(str)
for ns in nouns:
    try:
        ns_n_dict[ns] = n_count[ns[:-1]]
##        ns_n_dict[ns] = n_fd[ns[:-1]]
    except: pass

nns_hits = [ns for ns in ns_n_dict.keys() if ns_count[ns]>ns_n_dict[ns]]


# 17 Lookup tagger
POScdict = nltk.defaultdict(lambda: nltk.defaultdict(int))
for (w1, t1) in gold.tagged_words():
    POScdict[w1.lower][t1] += 1
frac_count_dict = nltk.defaultdict(tuple)

for key in POScdict.keys():
    temp = []
    for s_key in POScdict[key].keys():
        temp.append(POScdict[key][s_key])
    frac_count_dict[key] = (float(max(temp)), sum(temp))

numWords = len(gold.tagged_words())
overallPerf = 1
for key in frac_count_dict.keys():
    overallPerf *= frac_count_dict[key][0]/float(len)
print overallPerf

# 18
# create dict for num of words with [key] POS different tags
# and create bool dict for word having > 1 POS tag
    # a, b
tagtypecount = nltk.defaltdict(int)
ambigdict = nltk.defaultdict(bool)
for key in POScdict.keys():
    num = len(POScdict[key].keys())
    tagtypecount[num] += 1
    ambigdict[key] = (num>1)
    # c
ambig_count = 0
for word in brown.words:
    ambig_count += int(ambigdict[word.lower])
frac_ambig = float(ambig_count)/len(brown.words)

# 20
mdList = sorted(set(word.lower() for (word,tag) in\
                    brown.tagged_words() if tag=='MD'))
plnouns = sorted(set(word.lower() for (word,tag) in\
                    brown.tagged_words() if\
		    tag.startswith('NNS')))
doupa = set(plnouns.intersection(set(treperv)))
    # c
prepPhraz = sorted(set((w1.lower(), w2.lower(), w3.lower()) \
		     for ((w1, t1), (w2, t2), (w3, t3)) in \
		     nltk.itrigrams(brown.tagged_words()) if \
		     (t1=='IN' and t2.startswith('DT') and pattern03.match(t3))))
    # d
countM = len([word.lower() for (word, tag) in brown.tagged_words() if \
              tag.startswith('PPS') and word.lower().startswith('he')])
countF = len([word.lower() for (word, tag) in brown.tagged_words() if \
              tag.startswith('PPS') and word.lower().startswith('she')])


# 39: Stat taggers
fd_tagbrown = nltk.FreqDist(nltk.bigrams(tag for\
                                         (word, tag) in brown.tagged_words()))
