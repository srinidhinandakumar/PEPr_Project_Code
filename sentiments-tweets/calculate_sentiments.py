import json
import matplotlib.pyplot as plt
import nltk
import re

from collections import Counter
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
# from vaderSentiment import sentiment as vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict

class CalculateSentiments:
    def __init__(self):
        self.inputfilename = "../twitter_scraper/data/alltweets.json"
        self.outputfolder = "topic_sentiments/sentiments.json"

        self.topic_polarity = defaultdict(float)
        self.analyser = SentimentIntensityAnalyzer()

    def get_tweet_topics(self, tweet):
        topics = {0: 0.2, 1: 0.5, 2: 0.3} # [0.2, 0.5, 0.3]
        return topics

    def polarity(self, sentence):
        sentiment = self.analyser.polarity_scores(sentence)
        print(sentiment)
        return sentiment

    def add_to_topic_polarity(self, topics, sentiments):
        # topics: {0: 0.2, 1: 0.5, 2: 0.3}
        # sentiments: {'neg': 0.0, 'neu': 0.256, 'pos': 0.744, 'compound': 0.4404}

        pass

    def main(self):
        try:
            with open(self.inputfilename, "r") as fr:
                lines = fr.readlines()
                for line in lines:
                    tweet = json.loads(line)
                    tweet_text = tweet["full_text"]

                    # Hit topic modeling API to get topics and weights
                    topics = self.get_tweet_topics(tweet_text)

                    # Vader SentimentAnalyzer to finding the polarity of the tweet
                    sentiments = self.polarity(tweet_text)

                    # Multiply each topic-weight with polarity and add it to a final dictionary
                    self.add_to_topic_polarity(topics, sentiments)

        except FileNotFoundError:
            print("unable to find tweet file")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        CalculateSentiments().main()
    except KeyboardInterrupt:
        exit(0)

