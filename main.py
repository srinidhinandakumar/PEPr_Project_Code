
import re
import time
import json
import string
import datefinder
from textblob import TextBlob
from datetime import datetime as dt
from speech_ir.lda_models import lda_model
from tweets_clean.clean_tweets import cleaning_pipeline


inputfilename = "../twitter-scraper-rohith/data/10ktweets.json"
outputfilename = "../twitter-scraper-rohith/cleaned_data/10ktweets.json"


def main(ldamodel):
    try:
        result = ""
        count=0
        start=False
        tweet_id_prev=756633551152394240
        fq = open(outputfilename, "a")
        start = list(datefinder.find_dates("Sat Sept 24 00:00:00 +0000 2016"))[0]
        end = list(datefinder.find_dates("Fri Sept 30 23:59:59 +0000 2016"))[0]
        with open(inputfilename, "r") as fr:
            lines = fr.readlines()
            for line in lines:
                try:
                    tweet = json.loads(line)
                    '''
                    On rerunning from a previous tweet - update tweet_id_prev and uncomment following code
                    '''
                    # if tweet["id"]!=tweet_id_prev and not start:
                    #   continue
                    # else:
                    #   start = True
                    '''
                    Dump only texts 
                    '''
                    match = list(datefinder.find_dates(tweet["created_at"]))[0]
                    if start<=match<=end:
                        print(tweet["id"])
                        cleaned_tweet = cleaning_pipeline(tweet["full_text"])
                        fq.write(cleaned_tweet)
                        fq.write("\n")
                    '''
                    Dump entire tweet json 
                    '''
                    # print(tweet["id"])
                    # cleaned_tweet = cleaning_pipeline(tweet["full_text"])
                    # tweet["full_text"] = cleaned_tweet
                    # json.dump(tweet, fq)
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

    except FileNotFoundError:
        print("unable to find tweet file")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    t = time.time()
    print("----Creating LDA Model-----")
    ls = lda_model()
    t1 = time.time()
    print(str(t1-t))
    main(ls)
    print(time.time()-t1)
