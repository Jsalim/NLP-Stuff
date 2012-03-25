import nltk

# Basic stuff from the book

def plural(word):
    if word.endswith('y'):
        return word[:-1]+'ies'
    elif word[-1] in ['sx'] or word[-2] in ['sh','ch']:
        return word + 'es'
    elif word.endswith('an'):
        return word[:-2] + 'en'
    else:
        return word+'s'

def unusual_words(text):
    text_vocab = set(w.lower() for w in text if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    unusual = text_vocab.difference(english_vocab)
    return sorted(unusual)

def content_fraction(text,opt = 'frac'):
    from nltk.corpus import stopwords
    
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in text if w.lower() not in stopwords]
    if opt == 'frac':
        return len(content) / len(text)
    elif opt == 'set':
        return content
    else:
        return len(content) / len(text)

#My T9 program...input numbers from keypad, spits out possible
#words and most popular word beginnings from typed text
def T9search(nums):
    import re
    wordlist = [w for w in nltk.corpus.words.words('en') if w.islower()]
    on="[.!?']"
    tw='[abc]'
    th='[def]'
    fo='[ghi]'
    fi='[jkl]'
    sx='[mno]'
    se='[pqrs]'
    oc='[tuv]'
    ni='[wxyz]'
    but2num = {"1":on,"2":tw,"3":th,"4":fo,
               "5":fi,"6":sx,"7":se,"8":oc,
               "9":ni}
    searchStr = ''
    DefaultStr = ''
    for nummer in nums:
        searchStr = searchStr+but2num[nummer]
        DefaultStr = DefaultStr+but2num[nummer][1]
    #Search for words with the specified criteria
    pos_list = [w for w in wordlist if
                re.search("^"+searchStr+"$",w)]
    #Search for words that start with specified letters
    str_list = [w[0:len(nums)] for w in wordlist if
                re.search("^"+searchStr,w)]
    str_list_u = sorted(set(str_list))
    if len(str_list_u)>0:
        num_occ = [str_list.count(tag) for tag in str_list_u]
        word_ret = str_list_u[num_occ.index(max(num_occ))]
    else:
        word_ret = DefaultStr
    #Assign the first letter values if no strings found
    if len(pos_list)==0:
        pos_list = DefaultStr
    #Return word list
    return pos_list, word_ret
