
# coding: utf-8

# In[1]:

import time
import re
import json
from textblob import TextBlob
import string

from speech_ir.lda_models import lda_model
from tweets_clean.clean_tweets import cleaning_pipeline

# In[14]:


inputfilename = "../twitter-scraper-rohith/data/1000tweets.json"
outputfilename = "../twitter-scraper-rohith/cleaned_data/1000tweets.json"


def main(ldamodel):
    try:
        result = ""
        count=0
        allc = 0
        start=False
        tweet_id_prev=756633551152394240
        fq = open(outputfilename, "a")
        with open(inputfilename, "r") as fr:
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
                    cleaned_tweet = cleaning_pipeline(tweet["full_text"])
                    tweet["full_text"] = cleaned_tweet
                    json.dump(tweet, fq)
                    # count+=1
                    # if count==800:
                    #     allc+=count
                    #     print("*****Cleaned ",allc," tweets*****")
                    #     with open(outputfilename, "a") as fq:
                    #         fq.write(result)
                    #     result=""
                    #     count=0

                except Exception as e:
                    print("Error : "+str(e))
        # write into output folder and file
        print(result)
        with open(outputfilename, "a") as fq:
            fq.write(result)
            # may be we'll use this file for predicting polarity and topic modelling

    except FileNotFoundError:
        print("unable to find tweet file")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    t = time.time()
    print("----Creating LDA Model-----")
    ls = lda_model()
    print(str(time.time()-t))

    main(ls)
