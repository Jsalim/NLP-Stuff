import sys, os, nltk, random
from nltk.corpus import movie_reviews
documents = [(list(movie_reviews.sents(fileid)), category)
	     for category in movie_reviews.categories()
	     for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
all_bigrams = nltk.FreqDist((w1.lower(),w2.lower()) for sent in \
			    movie_reviews.sents() for (w1, w2) in \
			    nltk.bigrams(sent))
word_features = all_words.keys()[:2000]
bigram_features = all_bigrams.keys()[:2000]


def document_features(document):
    document_words = set(word for sent in document for word in sent)
    document_bigrams = set(bg for sent in document \
                           for bg in nltk.bigrams(sent))
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    for bigram in bigram_features:
        features['contains bigram(%s)' % str(bigram)] = \
                 (bigram in document_bigrams)
    return features
'''
Sentence classifier.  Goal is to break text up into sentences.  Use
punctuation marks to do so...
'''
# need to add stuff for mr. mrs., 'etc.', etc.

sents = nltk.corpus.treebank_raw.sents()
tokens = []
boundaries = set()
offset = 0
for sent in nltk.corpus.treebank_raw.sents():
    tokens.extend(sent)
    offset += len(sent)
    boundaries.add(offset-1)
	
def punct_features(tokens, i):
    return{'next-word-cap':tokens[i+1][0].isupper(),
	   'prevword':tokens[i-1].lower(),
	   'punct':tokens[i],
           'prev-word-is-one-char':len(tokens[i-1])==1,
           'followed-by-com': tokens[i+1]==','}

    
featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)

punct_pattern = re.compile('''(?!.*"|.*'|.*\.\.\.$)
[a-zA-Z0-9]*
(([\.\?\!]+(\)?)[\.\?\!]*)|
([\.\?\!]*(\)?)[\.\?\!]+))
''')
punct_pattern = re.compile('''
(?!.*"|.*'|.*\.\.\.$)   # exclude " and ...
[a-zA-Z]*               # may be paired w/ chars
[\.\?\!]+               # main match for punc
(\)?)                   # may be in ()
[\.\?\!]*$              # may have punc after )
                            ''')

featuresets = [(punct_features(tokens, i), (i in boundaries))
	       for i in range(1, len(tokens)-1)
	       if punct_pattern.match(tokens[i])]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)

def segment_sentences(words):
    start=0
    sents = []
    for i, word in enumerate(words[start:]):
        if punct_pattern.match(word) and \
            classifier.classify(punct_features(words, i))==True:
                sents.append(words[start:i+1])
                start = i+1
    if start < len(words):
        sents.append(words[start:])
    return sents

# alternatively, use nltk.sent_tokenize(raw)...
