import random
import nltk
from nltk.corpus import brown
from nltk.corpus import stopwords
from cPickle import dump
from pprint import pprint

train_dict = nltk.defaultdict(list)
test_dict = nltk.defaultdict(list)

def FDtoDIC(fd):
    out_dict = nltk.defaultdict(float)
    for key in fd.keys():
        out_dict[key] = fd[key]
    out_dict['N'] = fd.N()
    return out_dict


for category in set(brown.categories()).\
    difference(set(['humor', 'science_fiction'])):
    cat_files = brown.fileids(categories=category)
    random.shuffle(cat_files)
    size = int(len(cat_files) * 0.85)
    train, test = cat_files[:size], cat_files[size:]
    key_list = []
    for f in train:
        temp = brown.open(f).read().split()
        temp = [entry.split('/')[0] for entry in temp]
        temp = [entry for entry in temp if entry \
                not in stopwords.words('english')]
        train_dict[category].append(FDtoDIC(nltk.FreqDist(temp)))
        key_list.extend(train_dict[category][-1].keys())
    # compute the averge sample for the given category
    key_list = set(key_list)
    cat_avg_dict = {}
    for word in key_list:
        score = 0.0
        for fdd in train_dict[category]:
            score += float(fdd[word])/fdd['N']
        cat_avg_dict[word] = float(score) / len(train_dict[category].keys())
    train_dict[category].append(cat_avg_dict)

    for f in test:
        temp = brown.open(f).read().split()
        temp = [entry.split('/')[0] for entry in temp]
        temp = [entry for entry in temp if entry \
                not in stopwords.words('english')]
        test_dict[category].append(FDtoDIC(nltk.FreqDist(temp)))

train_out = open('trainKer01.pkl', 'wb')
dump(train_dict, train_out, -1)
train_out.close()
test_out = open('testKer01.pkl', 'wb')
dump(test_dict, test_out, -1)
test_out.close()

