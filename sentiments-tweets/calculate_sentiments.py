import json
import matplotlib.pyplot as plt
import nltk
import re

from collections import Counter
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

class CalculateSentiments:
    def __init__(self):
        self.inputfilename = "../twitter_scraper/data/alltweets.json"
        self.outputfolder = "topic_sentiments/sentiments.json"

    def main(self):
        try:
            with open(self.inputfilename, "r") as fr:
                lines = fr.readlines()
                for line in lines:
                    tweet = json.loads(line)
                    tweet_text = tweet["full_text"]

                    # Hit topic modeling API to get topics and weights

                    # Vader SentimentAnalyzer to finding the polarity of the tweet

                    # Multiply each topic-weight with polarity and add it to a final dictionary

        except FileNotFoundError:
            print("unable to find tweet file")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        CalculateSentiments().main()
    except KeyboardInterrupt:
        exit(0)

