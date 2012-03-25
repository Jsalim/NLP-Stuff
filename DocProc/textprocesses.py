import sys, os, re, nltk

# required that object be of <class 'nltk.text.Text'> type...
class TextProcess():
    def __init__(self, text, stops = [], language='english', ext=0):
        self.text = text
        self.content = self.getcontent()
        if ext:
            self.getExt()


    def getconcord(self, word, width=60, lines=25):
        func = (lambda word=word, width=width, lines=lines:
                      self.text.concordance(word, width, lines))
        text = self.cmdgrab(func)
        return text[1:]

    def getsimilar(self, word, N=20):
        func = (lambda word=word, N=N:
                self.text.similar(word, N))
        sims = self.cmdgrab(func)
        outSims = []
        for e in sims:
            outSims.extend(e.split(' '))
        return outSims

    def getcomcontext(self, words, N=20):
        func = (lambda words=words, N=N:
                self.text.common_contexts(words, N))
        text = self.cmdgrab(func)
        text = text[0].split()
        return text
        
    def getcolloc(self, N=20, window=2):
        func = (lambda N=N, window=window:
                self.text.collocations(N, window))
        text = self.cmdgrab(func)[1:]
        text = (';'.join(text)).split(';')
        return text

    def cmdgrab(self,func):
        try:
            fd = open('__temp.txt', 'w+')
            temp = sys.stdout
            sys.stdout = fd
            func()
            fd.flush()
            fd.seek(0,0)
            text = [line[:-1] for line in fd.readlines()]
        except:
            text = None
        finally:
            fd.close()
            os.remove('__temp.txt')
            sys.stdout = temp
            return text
        
    def getExt(self, stops = []):
        self.content = self.getcontent(stops=stops, language=language)
        self.fd = nltk.FreqDist(text)
        self.vocab = self.getvocab()


    def getcommonends(self, txt='content', N=10, maxwind=3, minwind=2):
        temp = []
        text = self.content if txt=='content' else self.text
        for k in range(minwind, maxwind+1):
            temp.extend([w[-k:] for w in text if len(w)>k])
        return nltk.FreqDist(temp)

    def getcontent(self, stops=[], language='english'):
        sws = nltk.corpus.stopwords.words(language)
        sws.extend(stops)
        return [w for w in self.text if w.lower() not in sws]

    def content_fraction(self, stops=[]):
        if len(stops)!=0:
            stops = [stop.lower() for stop in stops]
            content = [w for w in self.content if w.lower() not in stops]
        else:
            content = self.content
        return float(len(content)) / float(len(self.text))

    def getvocab(self):
        return list(sorted(set(w.lower() for w in self.text)))
        
