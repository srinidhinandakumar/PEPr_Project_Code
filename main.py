import datefinder
import json
import matplotlib.pyplot as plt
import pandas as pd
import re
import string
import time

from collections import Counter
from datetime import datetime as dt
from textblob import TextBlob
from gensim import corpora, models, similarities
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# User defined library imports
from speech_ir.lda_models import build_lda_model, predict_topics, num_topics
from tweets_clean.clean_tweets import cleaning_pipeline

inputfilename = "../twitter-scraper-rohith/data/10ktweets.json"
outputfilename = "../twitter-scraper-rohith/cleaned_data/10ktweets.json"

cleaned_tweets_inputfile = "twitter_scraper/cleaned_data/10ktweets_cleaned.txt"


import nltk
from nltk.tokenize.toktok import ToktokTokenizer
tokenizer = ToktokTokenizer()

stopword_list = nltk.corpus.stopwords.words('english')


def cleaning():
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


def remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def main(lda_model, dictionary):
    features = pd.read_csv(cleaned_tweets_inputfile)
    # print(features)

    tweet_dictionary = {}
    id = 0
    for tweet in features.text:
        tweet_dictionary[id] = tweet
        id += 1
    # print(tweet_dictionary[1])

    analyser = SentimentIntensityAnalyzer()
    topic_sentiments = {}

    for i in range(0, len(features)):
        snt = analyser.polarity_scores(tweet_dictionary[i])
        features.at[i, 'vader_comp'] = snt['compound']
        features.at[i, 'vader_pos'] = snt['pos']
        features.at[i, 'vader_neu'] = snt['neu']
        features.at[i, 'vader_neg'] = snt['neg']
        features.at[i, 'topic'] = predict_topics(tweet_dictionary[i], lda_model, dictionary)

    # print(features)

    num_tweets = len(features)
    vad_num_pos = len(features[features['vader_comp'] > .1])
    vad_num_neg = len(features[features['vader_comp'] < -.1])
    vad_num_neu = len(features[(features['vader_comp'] < .1) & (features['vader_comp'] > -.1)])

    print("vad_num_pos: %d\nvad_num_neg: %d\nvad_num_neu: %d\ntotal: %d\n" %(vad_num_pos, vad_num_neg, vad_num_neu, num_tweets))

    make_chart(vad_num_pos, vad_num_neg, vad_num_neu)
    get_10_most_neg_tweets(analyser, tweet_dictionary)

    # Some topics are more positive / negative than others
    topic = list(range(0, num_topics))
    # plt.figure(figsize=(20, 8))

    for i in topic:
        # plt.subplot(1, num_topics, i + 1)
        topic_tweets = features[features['topic'] == i]
        num_pos = len(topic_tweets[topic_tweets['vader_comp'] > .1])
        num_neg = len(topic_tweets[topic_tweets['vader_comp'] < -.1])
        num_neu = len(topic_tweets[(topic_tweets['vader_comp'] < .1) & (topic_tweets['vader_comp'] > -.1)])
        make_chart(num_pos, num_neg, num_neu, i)

    # plt.show()


def get_10_most_neg_tweets(analyser, tweet_dictionary):
    scores = Counter()
    for idx, tw in enumerate(tweet_dictionary.values()):
        snt = analyser.polarity_scores(tw)
        scores[tw] = (idx, snt['neg'])

    scores = [(key, val) for key, val in scores.items()]
    scores.sort(key=lambda x: x[1][1], reverse=True)

    print(scores[:10])

def make_chart(positve, negative, neutral, source= "Raw"):
    # Pie chart
    labels = ['positive','negative','neutral']
    sizes = [positve, negative, neutral]
    colors = ['#99ff99','#ff9999','#66b3ff']
    explode = (0.05,0.05,0.05)
    plt.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=80, pctdistance=.9, explode = explode,textprops={'fontsize': 12})

    #draw circle
    centre_circle = plt.Circle((0,0),0.55,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Sentiment Distribution for Topic '+str(source), size = 20)
    plt.axis('equal')
    # plt.imsave('topic_sentiments/topic_'+source+'.png', centre_circle)
    plt.show()
    # plt.close()


if __name__ == '__main__':
    t = time.time()
    print("----Creating LDA Model-----")
    ldamodel, dictionary = build_lda_model()
    t1 = time.time()
    print(str(t1-t))
    # cleaning(ls)

    for idx, topic in ldamodel.print_topics(-1):
        print('Topic: {} Word: {}'.format(idx, topic))

    main(ldamodel, dictionary)


    print("find polarity and ", time.time()-t1)
