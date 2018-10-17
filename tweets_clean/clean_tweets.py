
# coding: utf-8

# In[1]:


import re
import json
from textblob import TextBlob
import string


# In[14]:


inputfilename = "../twitter_scraper/data/alltweets.json"
outputfilename = "cleaned_data/alltweets.json"

with open("expansions.json", "r") as fp:
    cList = json.load(fp)
c_re = re.compile('(%s)' % '|'.join(cList.keys()))


# In[15]:


def strip_links(self, text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text


# In[16]:


def expandContractions(self, text):
    c_re=self.c_re
    def replace(match):
        return cList[match.group(0)]

    text = c_re.sub(replace, text.lower())
    return text


# In[17]:


def strip_hashtags(self, text):
    entity_prefixes = ['#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


# In[18]:


def strip_mentions(self, text):
    entity_prefixes = ['@']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


# In[19]:


def remove_special_characters(self, text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


# In[20]:


def spellcheck(self, text):
    b = TextBlob(text)
    correct_spelling = b.correct()
    return correct_spelling


# In[21]:


def cleaning_pipeline(self, text):
    text = self.spellcheck(text)
    #text = self.remove_special_characters(text)
    text = self.strip_mentions(text)
    text = self.strip_hashtags(text)
    text = self.expandContractions(text)
    text = self.strip_links(text)

    return text


# In[ ]:


def main(self):
    try:
        result = ""
        count=0
        allc = 0
        start=False
        tweet_id_prev=756633551152394240
        with open(self.inputfilename, "r") as fr:
            lines = fr.readlines()
            for line in lines:
            try:
                tweet = json.loads(line)
                # on rerunning from a previous tweet - update tweet_id_prev
                # if tweet["id"]!=tweet_id_prev and not start:
                #   continue
                # else:
                #   start = True

                print(tweet["id"])
                cleaned_tweet = self.cleaning_pipeline(tweet["full_text"])
                tweet["full_text"] = cleaned_tweet
                result+=str(tweet)+"\n"
                count+=1
                if count==800:
                    allc+=count
                    print("*****Cleaned ",allc," tweets*****")
                    with open(self.outputfilename, "a") as fq:
                        fq.write(result)
                    result=""
                    count=0
            except Exception as e:
                print("Error : "+str(e)+" "+print(tweet["id"]))
        # write into output folder and file
        print(result)
        with open(self.outputfilename, "a") as fq:
            fq.write(result)
            # may be we'll use this file for predicting polarity and topic modelling

    except FileNotFoundError:
        print("unable to find tweet file")
    except Exception as e:
        print(e)


# In[ ]:


if __name__ == '__main__':
    try:
        CleanTweet().main()
    except KeyboardInterrupt:
        exit(0)

