import csv
import json
import matplotlib.pyplot as plt
import nltk
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib


from collections import Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud


inputfolder = "../../2016electionmemes/"
statsfolder = "stats/"
chartfolder = "charts/"

def plot_bar_chart(source_filename, count = 10, long_tail = False):
    plt.rcdefaults()

    with open(source_filename) as f:
        tweet_source_data = json.load(f)

    objects = []
    values = []

    for k, v in tweet_source_data.items():
        objects.append(k)
        values.append(v)

    objects = objects[:count]
    values = values[:count]

    y_pos = np.arange(len(objects))

    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, rotation=90)

    if long_tail: plt.savefig(chartfolder + source_filename.split("/")[-1] + "_all.png")
    else: plt.savefig(chartfolder + source_filename.split("/")[-1] + ".png")

    plt.show()

def dumpDict(dic, loc, sort = True, key = 1):
    if sort:
        dic = dict(sorted(dic.items(), key=lambda x: -int(x[key])))

    with open(loc, 'w') as fp:
        json.dump(dic, fp)

def countMemes():
    meme_count = {}
    for file in os.listdir(inputfolder):
        filepath = inputfolder + file
        meme_count[file] = getLines(filepath)

    outputfilename = statsfolder + 'counts.json'
    dumpDict(meme_count, outputfilename)
    plot_bar_chart(outputfilename)

def getLines(self, fname):
    with open(fname, 'r', encoding="ISO-8859-1") as f:
        for i, l in enumerate(f): pass
    return i + 1

def meme_time():
    # my_cols = ["timestamp", "id", "link", "caption", "author", "network", "likes"]

    for file in os.listdir(inputfolder):
        filepath = inputfolder + file
        if file == "Donald.csv":
            continue

        df = pd.read_csv(filepath, engine='python')
        # df = df.drop(df.ix[:, 'Unnamed: 7':'Unnamed: 199'].head(0).columns, axis=1)
        timestamps = df.timestamp.dropna()
        # df = df.reset_index(drop=True)

        # print(df.head(5))
        # print(timestamps.head(5))

        dates = []
        min_date, max_date = datetime.now().strftime('%Y%m%d'), (datetime.now() - relativedelta(years = 10)).strftime('%Y%m%d')
        for line in timestamps:
            try:
                datetime_object = datetime.strptime(str(line), '%m/%d/%y %H:%M').strftime('%Y%m%d') #10/11/16 15:00
                # print(datetime_object)
                dates.append(datetime_object)
                min_date = min(min_date, datetime_object)
                max_date = max(max_date, datetime_object)
            except Exception as e:
                continue
        # print(dates)

        date_count_dict = Counter(dates)

        outputfilename = statsfolder + "dates_" + file + '.json'
        dumpDict(date_count_dict, outputfilename, sort = True, key = 0)
        plot_bar_chart(outputfilename, count = 30)
        plot_bar_chart(outputfilename, count = len(date_count_dict), long_tail = True)
        print("{0}: {1} to {2}".format(file, min_date, max_date))

        # break

def getAllMemesBetween(start, end):
    pass


def sentiment():
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyser = SentimentIntensityAnalyzer()

    sentence = "ooooo ROGERS 11:47 PM\n T 25%\n upandoutcomic\n Bernie feel the bern.usa\n Our strategy to win\n is quite simple.\n SUPERCALIFORNLOGISTICS\n EXPIALIDELEGATESTI\n 68 likes\n COO"
    sentence_wo = "ooooo ROGERS 11:47 PM T 25% upandoutcomic Bernie feel the bern.usa Our strategy to win is quite simple. SUPERCALIFORNLOGISTICS EXPIALIDELEGATESTI 68 likes COO"
    sentence_1 = "When you accidentally Bern your\n toast"
    print(str(analyser.polarity_scores(sentence)))
    print(str(analyser.polarity_scores(sentence_wo)))
    print(str(analyser.polarity_scores(sentence_1)))


# countMemes()
# sentiment()
meme_time()