import sys, os
from bs4 import BeautifulSoup as bs
import urllib2

# self-reference reference
url = "http://www.crummy.com/software/BeautifulSoup/bs4/doc/"
soup = bs(urllib2.urlopen(url).read())

# get stuff, like paragraphs
tag = soup.p
print tag
print tag.name      # returns 'p'
tag.name = 'paragraph'
print tag.name      # wonder what it returns now....
print tag           # bet you didn't think this would change too, eh?

tag = soup.a
print tag.attrs     # dictionary keys for attrs associated with 'a' block

# more random examples...
soup.a.text[-50:]
soup.h1.text[-50:]
soup.table.text[-50:]
soup.b.text[-50:]
soup.p.text[-50:]
soup.tr.text[-50:]

# slide easily down the rabbit hole....
soup.head.meta.attrss
# don't want just one...
soup.find_all('a')

'''Getting contents / children and descendents'''
print len(soup.contents)    # in this case, the 2nd entry is main doc
print len(soup.contents[1].contents)
print soup.contents[1].contents[0].text

head_tag = soup.head
title_tag = head_tag.contents[0]
for child in head_tag.children:
    print(child)

for child in head_tag.descendants:
	try: print child
	except RuntimeError:
            print 'Bottomed out\n' # have to block against this
# the difference:
print(len(list(soup.children)))
print(len(list(soup.descendants)))

# another "trick"
print(title_tag.string)     #--> no content? just string
print(head_tag.string)      #--> content?  no string

'''Iterators of the next two methods are the same thing, just plural'''
# parents also exist
print(title_tag.parent)

# as do siblings (tags at the same intendation level..)
title_tag.next_sibling
title_tag.next_sibling.next_sibling
