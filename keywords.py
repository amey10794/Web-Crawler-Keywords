import re
import requests
from bs4 import BeautifulSoup
import nltk
from nltk import bigrams
from nltk.stem import WordNetLemmatizer
from user_agent import generate_user_agent
import copy
from string import digits
import sys


headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('linux'))}

class keywords:
    def __init__(self,url):
        try:
            page = requests.get(url,headers=headers)
            if page.status_code!=200:

                sys.exit()

        except:
            raise ValueError('Unable to get content from '+ url)

        try:

            soup = BeautifulSoup(page.content, 'html.parser')
        except:
            raise ValueError('Unable to parse url')
        self.soup=soup

    #-------------Processing of text as needed
    #    input: String
    #    output: String
    def textPros(self,text):
        text=text.lower()
        text = re.sub(r'([^\s\w-]|_|\n|\t|\r)+', ' ', text)

        return text
    #-------------------Get all the headings in the url
    def getHeadx(self):
        ans = ""

        tag = self.soup.find("h1")
        if tag != None:
            ans+=self.textPros(tag.get_text())
            ans+=" "
        tag = self.soup.find("h2")
        if tag != None:
            ans+=self.textPros(tag.get_text())
            ans += " "
        tag = self.soup.find("h3")
        if tag != None:
            ans+=self.textPros(tag.get_text())
            ans += " "
        tag = self.soup.find("h4")
        if tag != None:
            ans+=self.textPros(tag.get_text())
            ans += " "
        tag = self.soup.find("h5")
        if tag != None:
            ans += self.textPros(tag.get_text())
            ans += " "
        tag = self.soup.find("h6")
        if tag != None:
            ans += self.textPros(tag.get_text())
            ans += " "


        return ans


    #-------------- Get the title tag of the url
    def getTitle(self):
        tag = self.soup.find("title")
        if tag != None:
            return self.textPros(tag.get_text())
        else:
            return ""
    #---------------- Get the keywords meta if available
    def getKeywords(self):
        tag = self.soup.find("meta", {"name": "keywords"})
        if tag !=None:
            return self.textPros(tag.get_text())
        else:
            return ""


    #------------------Get the description meta if available
    # output: processed String or empty string
    def getDescription(self):
        tag = self.soup.find("meta", {"name": "description"})
        if tag != None:
            return self.textPros(tag['content'])
        else:
            return ""
    #-------------------Get the content of the url
    def getContent(self):
        tag = self.soup.find_all('p')
        content = ""
        if tag!=None:
            for t in tag:
                content += t.get_text().rstrip('\n')
            return self.textPros(content)
        else:
            return ""


    #------------------Load the stopwords from stopwords.txt
    def loadStopwords(self):
        file=open("stopwords.txt", "r")
        stopwords = file.read()
        stopwords = stopwords.split('\n')
        file.close()
        return stopwords

    #------------------- remove the stopwords from given string
    def removeStopwords(self,text):
        stopwords=self.loadStopwords()
        removed_string=""
        for word in stopwords:

            word = r'\b%s\b' % (word)
            iterable = re.finditer(word, text)
            # print(ab)
            for iter in iterable:
                # print(it)
                text = re.sub(word, '', text)
        return text

    #-------------------- perform Lemmatization on input string
    def doLemmatize(self,text):
        wordnet_lemmatizer = WordNetLemmatizer()
        tokens = self.getWordTokens(text)
        lemaout = ""
        for w in tokens:
            lemaout += wordnet_lemmatizer.lemmatize(w)
            lemaout += " "
        return lemaout


    #----------------------- tokenize words
    def getWordTokens(self,text):
        tokens = nltk.word_tokenize(text)
        return tokens

    #------------------------ sort bag of words given as input
    def getSortedBag(self,bag):
        sorted_bag = sorted(bag.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_bag

    #------------------------- use input tokens(unigrams) to get Word Density scores
    def getUnigrams(self,tokens):
        bags = {}
        for token in tokens:
            if (token in bags):
                bags[token] += 1
            else:
                bags[token] = 1

        return bags

    #---------------------------- use input tokens(unigrams) to get bigram based keyword scores
    def getBigrams(self,tokens):
        string_bigrams = bigrams(tokens)
        bibags = {}

        for gram in string_bigrams:
            if (gram in bibags):
                bibags[gram] += 1
            else:
                bibags[gram] = 1
        sorted_bibags=self.getSortedBag(bibags)
        return sorted_bibags

    #------------------------------- Double the bigram keyword scores and Add to unigrambags
    def addBigramstoBags(self,sorted_bibags,bags):

        if (sorted_bibags[0][1] > 1):
            biWords = [y for x in sorted_bibags for y in x[0] if x[1] == sorted_bibags[0][1]]
            for biWord in biWords:
                bags[biWord] *= 2
        return bags

    #--------------------------- Merge two bags together
    def getMergeBag(self,bag1,bag2):
        new_bag=copy.deepcopy(bag1)
        for key,value in bag2.items():
            if key in new_bag.keys():
                new_bag[key]+=value
            else:
                new_bag[key]=value
        return new_bag

    #--------------------------- Transform the input url
    def getTransformedURL(self,url):
        urls = url.split("/")
        Urls = ""
        for u in urls[2:]:
            Urls += u
            Urls += "\n"
        Urls = Urls.lower()
        Urls = re.sub(r'([^\s\w]|[\d] |_|\t|\r)+', ' ', Urls)
        remove_digits = str.maketrans('', '', digits)
        Urls = Urls.translate(remove_digits)
        return Urls



