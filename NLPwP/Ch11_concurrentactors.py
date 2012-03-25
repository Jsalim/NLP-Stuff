import nltk
from nltk.etree.ElementTree import ElementTree


def enterAct(details, ppl_on_stage, incidence_list):
    for ppl in details:
        if ppl.lower() != 'with':
            ppl = mapping[ppl.upper()]
            ppl_on_stage.append(ppl)
            for per in ppl_on_stage[:-1]:
                if (ppl, per,) not in incidence_list \
                   and (per, ppl,) not in incidence_list:
                    incidence_list.append((ppl, per,))
                    incidence_list.append((per, ppl,))
                    stage_cfd[ppl].inc(per)
                    stage_cfd[per].inc(ppl)
    return ppl_on_stage, incidence_list
            

def exitAct(details, ppl_on_stage, incidence_list):
    if len(ppl_on_stage) > 0:
        ppl_on_stage = ppl_on_stage[:-1]
        if len(details) > 0:
            if details[0].lower()=='with':
                for ppl in details[1:]:
                    try: ppl_on_stage.remove(mapping[ppl].upper())
                    except ValueError: pass
            elif len(details)==1:
                ppl_on_stage = ppl_on_stage[:-1]
            else:
                for ppl in details:
                    try: ppl_on_stage.remove(mapping[ppl].upper())
                    except ValueError: pass
    else:
        ppl_on_stage, incidence_list = exeuntAct()
    return ppl_on_stage, incidence_list

def exeuntAct():
    return [], []
    
'''
Prep stuff for doing the rest of this...
'''
# get the file and such
merchant_file = nltk.data.find('corpora/shakespeare/merchant.xml')
merchant = ElementTree().parse(merchant_file)
# people
speaker_seq = [s.text.upper() for s in \
               merchant.findall('ACT/SCENE/SPEECH/SPEAKER')]
speaker_freq = nltk.FreqDist(speaker_seq)
top10 = speaker_freq.keys()[:10]
mapping = nltk.defaultdict(lambda: 'OTHE')
for s in top10:
    mapping[s] = s[:4].upper()
# stage actions
stage_seq = [s.text for s in merchant.findall('ACT/SCENE/STAGEDIR')]
for i, stage in enumerate(stage_seq):
    stage_seq[i] = nltk.word_tokenize(stage)
keep_list = speaker_freq.keys()
keep_list.extend(['EXIT', 'ENTER', 'EXEUNT', 'WITH'])
for i, entry in enumerate(stage_seq):
    temp = []
    for ele in entry:
	if ele.upper() in keep_list:
	    temp.append(ele)
    stage_seq[i] = temp

'''
Main task goes on here...iteate over stage direction entries, parse
what they 'mean', update cdf.
'''
ppl_on_stage = []
incidence_list = []
stage_cfd = nltk.ConditionalFreqDist()

for entry in stage_seq:
    if len(entry) > 0:
        if entry[0].upper()=='ENTER':
            ppl_on_stage, incidence_list = \
              enterAct(entry[1:], ppl_on_stage, incidence_list)
        elif entry[0].upper()=='EXIT':
            ppl_on_stage, incidence_list = \
              exitAct(entry[1:], ppl_on_stage, incidence_list)
        elif entry[0].upper()=='EXEUNT':
            if len(entry)>1:
                ppl_on_stage, incidence_list = \
                  exitAct(entry[1:], ppl_on_stage, incidence_list)
            else:
                ppl_on_stage, incidence_list = exeuntAct()

stage_cfd.tabulate()
