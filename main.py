import re
from bs4 import BeautifulSoup
import requests
from keywords import *
from string import digits
from nltk import trigrams


#------------------ Input URL --------------------#
url=input("Please enter the url to be parsed: ")
url=url.strip()
if len(url)<1: url="https://www.rei.com/blog/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors"
if not (url.startswith('https://') or url.startswith('http://')): url="http://"+url

#------------------ Get HTML --------------------#
page=keywords(url)


#------------------ Get Necessary Data --------------------#
Urls=page.getTransformedURL(url)
title=page.getTitle()
keywords=page.getKeywords()
description=page.getDescription()
headings=page.getHeadx()
content=page.getContent()
meta=title + " " + keywords + " " + headings + " " + description + " " + Urls


#------------------ Process Content of the page --------------------#
content=page.removeStopwords(content)
content=page.doLemmatize(content)
tokens=page.getWordTokens(content)
bags=page.getUnigrams(tokens)
bibags=page.getBigrams(tokens)
content_bags=page.addBigramstoBags(bibags,bags)




#------------------ Process the Meta's --------------------#
meta=page.removeStopwords(meta)
meta=page.doLemmatize(meta)
tokens=page.getWordTokens(meta)
bags=page.getUnigrams(tokens)
bibags=page.getBigrams(tokens)
meta_bags=page.addBigramstoBags(bibags,bags)
meta_bags_sorted = page.getSortedBag(meta_bags)

#------------------ Merge the Content and Meta Bags --------------------#
merged_bag=page.getMergeBag(content_bags,meta_bags)

#------------------ Triple the Score for Meta keywords --------------------#
for keywords in meta_bags_sorted[:5]:
   if keywords[0] in merged_bag.keys():
       merged_bag[keywords[0]]*=3
   else:
       merged_bag[keywords[0]]=meta_bags[keywords[0]]*3
merged_bag_sorted = page.getSortedBag(merged_bag)


#-------------------- The final Keywords Result --------------------------#
print("For URL:"+ url)
key=[]
for keywords in merged_bag_sorted[:5]:
   key.append(keywords[0])
print("Keywords",key)
