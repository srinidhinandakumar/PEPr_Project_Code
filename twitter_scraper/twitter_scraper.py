import json
import time
from typing import List

import tqdm as tqdm
from tweepy import OAuthHandler, API

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


class TwitterScraper:
    def __init__(self):
        self.inputfilename = "data/tweetids.txt"
        self.outputfilename = "data/alltweets.json"
        self.lastidfilename = "data/lastId.txt"
        self.errorfilename = "data/errortweets.txt"
        self.request_rate_limits = 800
        self.api = self.authenitcate()

    def authenitcate(self):
        auth = OAuthHandler(consumer_key=consumer_key,
                            consumer_secret=consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = API(auth)
        return api

    def read_tweetIds(self):
        with open(self.inputfilename, "r") as fp:
            return fp.read().split("\n")

    def print_crawled_status(self):
        try:
            with open(self.outputfilename, "r") as fp:
                print("crawled {} tweets".format(len(fp.readlines())))
        except FileNotFoundError:
            print("unable to find output file, looks like crawler is starting "
                  "fresh")
        except Exception as e:
            print(e)

    def get_last_crawled_id(self):
        try:
            with open(self.lastidfilename, "r") as fq:
                tid = fq.read()
                return tid if tid.isnumeric() else None
        except FileNotFoundError:
            return None

    def append_tweets_data(self, json_tweets_list: List[str]):
        with open(self.outputfilename, 'a') as fp:
            fp.write("\n".join(json_tweets_list) + "\n")

    def write_last_id(self, lastId):
        with open(self.lastidfilename, 'w') as fp:
            fp.write(lastId)

    def write_error_tweets(self, error_tweets: List[str]):
        if error_tweets:
            with open(self.errorfilename, 'a') as fp:
                fp.write("\n".join(error_tweets) + "\n")

    def read_data(self):
        tweets = []
        with open(self.outputfilename, 'r') as fp:
            for json_tweet in fp.readlines():
                tweets.append(json_tweet)
        return tweets

    def scrap(self):
        tweetids = self.read_tweetIds()
        tweetids_count = len(tweetids)

        print("tweet ids to crawl: ", len(tweetids))
        self.print_crawled_status()

        lastId = self.get_last_crawled_id()
        start = tweetids.index(lastId) + 1 if lastId else 0
        print("crawling from ", start)

        # accumulators
        cur_cycle_tweets = []
        errorTweets = []
        cur_cycle_requests = 0
        crawled_tweets = 0
        for cycle in range(start, tweetids_count, self.request_rate_limits):
            # second loop to just show progress of crawling...
            for i in tqdm.tqdm(range(cycle, cycle+self.request_rate_limits)):
                try:
                    tweet = self.api.get_status(tweetids[i], tweet_mode="extended")
                    lastId = tweetids[i]
                    print(lastId)
                    cur_cycle_tweets.append(json.dumps(tweet._json))
                    crawled_tweets += 1
                except Exception as e:
                    print("------ERROR: ", str(e), " ID: ", tweetids[i], "------")
                    errorTweets.append(tweetids[i])
                    if type(e).__name__ == "RateLimitError":
                        print("------SLEEP for 200s------")
                        time.sleep(300)

            # at the end of cycle flushing everything to disk
            self.append_tweets_data(cur_cycle_tweets)
            self.write_error_tweets(errorTweets)
            self.write_last_id(lastId)
            cur_cycle_tweets = []
            errorTweets = []
            print("Cycle complete, crawled {} tweets".format(crawled_tweets))


if __name__ == '__main__':
    try:
        TwitterScraper().scrap()
    except KeyboardInterrupt:
        exit(0)

