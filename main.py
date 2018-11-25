import datefinder
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import string
import time
import csv
from collections import Counter
from datetime import datetime as dt
from textblob import TextBlob
from gensim import corpora, models, similarities
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from matplotlib.ticker import NullFormatter


# User defined library imports
from speech_ir.lda_models import build_lda_model, predict_topics, num_topics
from tweets_clean.clean_tweets import cleaning_pipeline


inputfilename = "../data/republican/republican.json"

output_tweet_filename = "../data/republican/republican_cleaned_tweets.txt"
output_meme_filename = "../data/republican/republican_cleaned_memes.txt"
output_all_filename = "../data/republican/republican_tweets_memes.txt"

cleaned_tweets_inputfile = "../data/republican/republican_tweets_memes.txt"
topic_sentiments_outputfolder = "../data/republican/topic_sentiments/"
'''
inputfilename = "../data/democratic/democratic.json"

output_tweet_filename = "../data/democratic/democratic_cleaned_tweets.txt"
output_meme_filename = "../data/democratic/democratic_cleaned_memes.txt"
output_all_filename = "../data/democratic/democratic_tweets_memes.txt"

cleaned_tweets_inputfile = "../data/democratic/democratic_tweets_memes.txt"
topic_sentiments_outputfolder = "../data/democratic/topic_sentiments/"
'''

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
tokenizer = ToktokTokenizer()

stopword_list = nltk.corpus.stopwords.words('english')

        
def clean_memes():
    inputfolder = "../data/republican/memes/"
    #inputfolder = "../data/democratic/memes/"
    fq = open(output_meme_filename, "a")
    files = ['Donald.csv','Trump.csv','Republican.csv']
    #files = ['Clinton.csv','Democrat.csv','Hillary.csv','imwithher.csv']
        
    try:
        for file in files:
            with open(inputfolder+file,encoding="utf-8") as fp:
                reader = csv.reader(fp)
                for row in reader:
                    #print(row[3]+"#####"+row[6])
                    fq.write(row[3]+"\t"+row[6])
                    fq.write("\n")
        print("Done!")
    except Exception as e:
        print("\n*********\n",str(e),"\n*********\n")
                
def cleaning():
    try:
        result = ""
        count=0
        start=False
        tweet_id_prev=756633551152394240
        fq = open(output_tweet_filename, "a")
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
                    Dump only texts between required dates
                    
                    match = list(datefinder.find_dates(tweet["created_at"]))[0]
                    if start<=match<=end:
                        print(tweet["id"])
                        cleaned_tweet = cleaning_pipeline(tweet["full_text"])
                        fq.write(cleaned_tweet)
                        fq.write("\n")
                    '''
                    
                    '''
                    Dump tweet texts
                    '''
                    print(tweet["id"])
                    cleaned_tweet = remove_stopwords(tweet["full_text"])
                    fq.write(cleaned_tweet+"\t"+str(tweet['user']['followers_count']))
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

def merge_files():
    tweets_data = open(output_tweet_filename,"r").read()
    memes_data = open(output_meme_filename,"r").read()
    
    open(output_all_filename,"w").write("text\treach\n"+tweets_data+memes_data)
    
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
    features = pd.read_csv(cleaned_tweets_inputfile,delimiter="\t")

    tweet_dictionary = {}
    id = 0
    for tweet in features.text:
        tweet_dictionary[id] = tweet
        id += 1

    analyser = SentimentIntensityAnalyzer()

    for i in range(0, len(features)):
        print(i)
        snt = analyser.polarity_scores(tweet_dictionary[i])
        features.at[i, 'tweet_id'] = i
        features.at[i, 'vader_comp'] = snt['compound']
        features.at[i, 'vader_pos'] = snt['pos']
        features.at[i, 'vader_neu'] = snt['neu']
        features.at[i, 'vader_neg'] = snt['neg']
        features.at[i, 'topic'] = predict_topics(tweet_dictionary[i], lda_model, dictionary)
        features.at[i, 'scaled_polarity'] = features.at[i,'vader_comp']*features.at[i,'reach']
    
    print(features)
    
    #features.to_csv('features_sentiments.csv')
    
    num_tweets = len(features)
    vad_num_pos = len(features[features['scaled_polarity'] > .1*features['reach']])
    vad_num_neg = len(features[features['scaled_polarity'] < -.1*features['reach']])
    vad_num_neu = len(features[(features['scaled_polarity'] < .1*features['reach']) & (features['scaled_polarity'] > -.1*features['reach'])])
    
    print("vad_num_pos: %d\nvad_num_neg: %d\nvad_num_neu: %d\ntotal: %d\n" %(vad_num_pos, vad_num_neg, vad_num_neu, num_tweets))
    
    #make_chart_2(features,vad_num_pos, vad_num_neg, vad_num_neu, num_topics)
    
    topic = list(range(0, num_topics))
    
    make_chart(vad_num_pos, vad_num_neg, vad_num_neu, num_topics)
    # get_10_most_neg_tweets(analyser, tweet_dictionary)

    for i in topic:
        # plt.subplot(1, num_topics, i + 1)
        topic_tweets = features[features['topic'] == i]
        vad_num_pos = len(topic_tweets[topic_tweets['scaled_polarity'] > .1*topic_tweets['reach']])
        vad_num_neg = len(topic_tweets[topic_tweets['scaled_polarity'] < -.1*topic_tweets['reach']])
        vad_num_neu = len(topic_tweets[(topic_tweets['scaled_polarity'] < .1*topic_tweets['reach']) & (topic_tweets['scaled_polarity'] > -.1*topic_tweets['reach'])])
        make_chart(vad_num_pos, vad_num_neg, vad_num_neu, num_topics, i)
    
    # plt.show()


def get_10_most_neg_tweets(analyser, tweet_dictionary):
    scores = Counter()
    for idx, tw in enumerate(tweet_dictionary.values()):
        snt = analyser.polarity_scores(tw)
        scores[tw] = (idx, snt['neg'])

    scores = [(key, val) for key, val in scores.items()]
    scores.sort(key=lambda x: x[1][1], reverse=True)

    print(scores[:10])

def make_chart(positve, negative, neutral, no_of_topics, source= "Raw"):
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
    # plt.show()
    plt.savefig(topic_sentiments_outputfolder + str(no_of_topics) + '/topic' + str(source) + '.png')
    plt.close()

def make_chart_2(features, positve, negative, neutral, no_of_topics, source= "Raw"):
    
    # plot positives, negatives and neutrals for all tweets
    x = features['vader_pos']
    y = features['tweet_id']
    features.plot(y='vader_pos',x='tweet_id',kind='line')
    #plt.plot(x,y,'r')
    #plt.axis([0, len(features), 0, 1])
    plt.show()


if __name__ == '__main__':
    
    t = time.time()
    print("----Creating LDA Model-----")
    ldamodel, dictionary = build_lda_model()
    
    t1 = time.time()
    print(str(t1-t))
    #ldamodel.save("lda.model")
    '''
    cleaning()
    clean_memes()
    merge_files()
    '''
    topic_info_file = topic_sentiments_outputfolder + str(3) + '/topics.txt'
    
    with open(topic_info_file, 'w') as fp:
        for idx, topic in ldamodel.print_topics(-1):
            fp.write('Topic: {} Word: {}\n'.format(idx, topic))
    
    main(ldamodel, dictionary)


    print("time taken", time.time()-t1)
    