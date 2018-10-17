
# coding: utf-8

# In[1]:


import re
import json
from textblob import TextBlob
import string

# In[14]:


# inputfilename = "../twitter_scraper/data/alltweets.json"
# outputfilename = "tweets_clean/cleaned_data/alltweets.json"
expansions = "tweets_clean/expansions.json"
# Sept 30

with open(expansions, "r") as fp:
    cList = json.load(fp)
c_re = re.compile('(%s)' % '|'.join(cList.keys()))


# In[15]:


def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text


# In[16]:


def expandContractions(text):
    global c_re

    def replace(match):
        return cList[match.group(0)]

    text = c_re.sub(replace, text.lower())
    return text


# In[17]:


def strip_hashtags(text):

    entity_prefixes = ['#','@']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] != "#":
                words.append(word)
    return ' '.join(words)


# In[18]:


def strip_mentions(text):
    entity_prefixes = ['@','#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] != "@":
                words.append(word)
    return ' '.join(words)


# In[19]:


def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


# In[20]:


def spellcheck(text):
    b = TextBlob(text)
    correct_spelling = b.correct()
    return correct_spelling


# In[21]:


def cleaning_pipeline(text):
    text = expandContractions(text)
    text = strip_links(text)
    text = strip_mentions(text)
    text = strip_hashtags(text)
    text = spellcheck(text)
    #text = remove_special_characters(text)

    return str(text)

# print(strip_hashtags("text1 text2 http://url.com/bla1/blah1/ #getup"))
# print(cleaning_pipeline("Hi @ieuehdbd https://scdjsd.com we're not coool #getup"))