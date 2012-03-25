import nltk
from cPickle import load
from pprint import pprint

train_in = open('trainKer01.pkl', 'rb')
train_dict = load(train_in)
train_in.close()
test_in = open('testKer01.pkl', 'rb')
test_dict = load(test_in)
test_in.close()

sim_scores = {}
for cat_test in test_dict.keys():
    sim_scores[cat_test] = nltk.defaultdict(float)
    for cat_train in train_dict.keys():
        train_fdd = train_dict[cat_train][-1]
        temp_sim_score = 0.0
        count = 0
        for fdd in test_dict[cat_test]:
            for word in fdd.keys():
                try:
                    temp_sim_score += float(fdd[word]) * \
                                      float(train_fdd[word])
##                                      float(len(train_dict[cat_train])-1)
                    count += 1
                except KeyError: pass
        temp_sim_score /= 10**5 * len(fdd.keys()) / float(count)
##        temp_sim_score /= float(len(test_dict[cat_test]))
        temp_sim_score = round(temp_sim_score, 2)
        sim_scores[cat_test][cat_train] = temp_sim_score


##sim_scores = {}
##for cat_test in test_dict.keys():
##    sim_scores[cat_test] = nltk.defaultdict(float)
##    for cat_train in train_dict.keys():
##        train_fdd = train_dict[cat_train][-1]
##        temp_sim_score = 0.0
##        for fdd in test_dict[cat_test]:
##            for word in fdd.keys():
##                try:
##                    temp_sim_score += float(fdd[word]) * \
##                                      float(train_fdd[word])
##                except KeyError: pass
##        temp_sim_score /= float(len(test_dict[cat_test]))
##        sim_scores[cat_test][cat_train] = temp_sim_score
##        print(cat_test, cat_train, temp_sim_score, end=' ')
##    print('\n')

output_list = [['Test Cat']]
for key in sim_scores:
    output_list.append([key])
    for key2 in sim_scores[key].keys():
        if len(output_list[0]) < len(sim_scores.keys()):
            output_list[0].append(key2)
        output_list[-1].append(sim_scores[key][key2])
for line in output_list:
    print line
