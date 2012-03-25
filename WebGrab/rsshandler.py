import sys, os, re, feedparser, nltk
from urllib import urlread

rssroll = [('physorg','http://www.physorg.com/rss-feed/'),
           ('bbc news - world','http://feeds.bbci.co.uk/news/world/rss.xml')]

class rssfeed():
    def __init__(self, feed):
        self.title = feed.title
        self.summary = self.getsummary(feed)
        self.link = feed.links[0]['href']

    def getsummary(self, feed):
        try:
            summary = nltk.word_tokenize(nltk.clean_html(feed.summary))
        except:
            summary = []
        return summary

    def getfullpost(self):
        try:
            raw = urlopen(self.link).read()
            tokens = nltk.word_tokenize(nltk.clean_html(raw))
        


for rss in rssroll:
    try:
        for post in feedparser.parse(rss[1]).entries:
            temp = rssfeed(post)
            

    except: pass
    
