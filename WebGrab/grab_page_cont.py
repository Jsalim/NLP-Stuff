import sys, os, nltk, math
from urllib import urlopen
from nltk.corpus import brown


contraction_dict = {"hasn't":'has not',"haven't":'have not',"hadn't":'had not',
                    "doesn't":'does not',"don't":'do not',"didn't":'did not',
                    "can't":'can not',"couldn't":'could not',
                    "isn't":'is not',"aren't":'are not',
                    "woln't":'will not', "wouldn't":'would not',
                    "shaln't":'shall not',"shouldn't":'should not',
                    "you'll":'you will',"she'll":'she will',
                    "they'll":'they will',"he'll":'he will',
                    "i'll":'i will',"we'll":'we will',"it'll":'it will',
                    "i'd":'i would',"he'd":'he would',"it'd":'it would',
                    "she'd":'she would',"you'd":'you would',
                    "we'd":'we would',"they'd":'they would',
                    "it's":'it is',"she's":'she is',
                    "he's":'he is', "i'm":'i am'}

'''
Attempt Num 1:  save patterns of simple tags found in sentences in brown,
and try and match sentences, as tokenized and tagged by NLTK's default stuff,
to said dictionary.  Below is the code to do this.  Hit rate is way way way
too low to inference anything reasonable.
'''
brown_tag_sent = brown.tagged_sents()
brown_tags = [[nltk.tag.simplify_brown_tag(tag) for \
         (word,tag) in sent] for sent in tag_brown]
##brown_tags = [[nltk.tag.simplify_tag(tag) for tag in sent] for \
##              sent in brown_tags]
temp = []
for sent in brown_tags:
    sub_temp = []
    for tag in sent:
        try:
            sub_temp.append(nltk.tag.simplify_tag(tag))
        except IndexError: pass
    temp.append(sub_temp)
joined_brown = [('-').join(sent) for sent in temp]
joined_brown = list(set(joined_brown))

matchVec = []
for sent in sents_tok:
    temp = nltk.tag.pos_tag(nltk.word_tokenize(sent))
    temp = ('-').join(nltk.tag.simplify_tag(tag) for (word,tag) in temp)
    try:
        joined_brown.index(sent)
        matchVec.append(1)
    except ValueError:
        matchVec.append(0)

'''
Attempt Num 2:  Create POS bigrams from brown (or something), and then create
CondFreqDist of bigram-bigram patterns (i.e., a FreqDist of trigrams...)
Use the found probabilities from sents in source doc to calc. "probability"
of a particular sentence structure.  Need some correction for sentence length
if a product of probs is used...
'''
brown_tag_sent = brown.tagged_sents()
brown_tags = [[nltk.tag.simplify_brown_tag(tag) for \
         (word,tag) in sent] for sent in tag_brown]
temp = []
for sent in brown_tags:
    sub_temp = []
    for tag in sent:
        try:
            sub_temp.append(nltk.tag.simplify_tag(tag))
        except IndexError: pass
    temp.append(sub_temp)

fd = nltk.FreqDist()
for sent in temp:
    if len(sent)>2:
        temp_tri = nltk.trigrams(sent)
        for entry in temp_tri:
            fd.inc(entry)
            
tfd = nltk.LidstoneProbDist(fd, gamma=1)
tfd_avg = sum(tfd.prob(sample) for sample in \
              tfd.samples()) / float(len(tfd.samples()))

raw = urlopen(url).read()
raw = nltk.clean_html(raw)
raw = raw.replace('\r\n', '')
raw = raw.replace('\n', '')
raw = raw.replace('\\', '')
raw = raw.lower()
for key in contraction_dict.keys():
    raw = raw.replace(key, contraction_dict[key])
sents_tok = nltk.sent_tokenize(raw)

matchVec = []
for sent in sents_tok:
    temp = nltk.tag.pos_tag(nltk.word_tokenize(sent))
    temp = [nltk.tag.simplify_tag(tag) for (word,tag) in temp]
    sent_len = len(temp)
    temp = nltk.trigrams(temp)
    score = 1.0
    for entry in temp:
        score *= (tfd.prob(entry)/tfd_avg)**(1.0/sent_len)
    matchVec.append(math.log(1+score))


'''
Attempt Num 3:  The smart way.  Actually looked at the HTML for a few different
pages.  Content all in <p>...</p> lines.  fucking joke...
'''

raw = urlopen(url).readlines()
content = []
for line in raw:
    if line.startswith('<p>'):
        content.append(line)
content = (' ').join(content)
content = nltk.clean_html(content)

'''
Attempt Num 4:  Modify the above slightly...need to grab stuff between <p> and
</p> occurances.  Still some "residual" extra crap on from most sites, but may
be easily removed if content analyzed, eh??
Comments are also sometimes included...
looks like social media share links come before this, though
'''
soc_med = ['facebook', 'myspace', 'digg', 'linkedin', 'twitter',
           'del.icio.us', 'stumbleupon']

raw = urlopen(url).read()
content = []
start = 0
while start < len(raw):
    ts = raw.find('<p', start)
    if ts != -1:
        tf = raw.find('</p>', ts)
        if tf != -1:
                content.append(raw[ts:tf+4])
                start = tf+4
            else:
                content.append(raw[ts:])
                start = len(raw)+22
        start = tf+4
    else: start = len(raw)*2
content = [ent for ent in content if ent.startswith('<p>')]
content = [nltk.clean_html(ent) for ent in content]
content = [ent for ent in content if ent != '']
content = [ent for ent in content if ent.lower() not in soc_med]


commentsMatch = re.compile(r'class=".*[C|c]omment.*">')
