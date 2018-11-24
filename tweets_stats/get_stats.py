import json
import matplotlib.pyplot as plt
import nltk
import re
import pprint

from collections import Counter
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

class GetStats:
    stop_words = set(stopwords.words('english'))

    def __init__(self):
        # self.inputfilename = "../twitter_scraper/data/alltweets.json"
        # self.inputfilename = "../twitter_scraper/data/dixita_alltweets.json"
        # self.inputfilename = "../twitter_scraper/data/sample_data.json"
        # self.inputfilename = "../twitter_scraper/data/srinidhi_alltweets.json"
        #self.inputfilename = "../../twitter-scraper-rohith/data/alltweets.json"
        #self.inputfilename = "../../twitter-scraper-akhil/data/alltweets.json"
        #self.inputfilename = "../../twitter-scraper-dixita/data/dixita_alltweets.json"
        #self.inputfilename = "../../twitter-scraper-srinidhi/data/alltweets.json"
        #self.inputfilename = "../../twitter-scraper-heet/data/heet_alltweets.json"
        ######
        #self.inputfilename = "../../data/democratic/democratic.json"
        self.inputfilename = "../../data/republican/republican.json"
        
        #self.outputfolder = "../../data/democratic/stats/"
        self.outputfolder = "../../data/republican/stats/"
        
        #self.chartouputfolder = "../../data/democratic/charts/"
        self.chartouputfolder = "../../data/republican/charts/"
        
        # Single Param dicts
        self.tweet_source_count = {}
        self.hashtag_count = {}
        self.date_count = {}
        #self.location_count_pos = {}
        #self.location_count_neg = {}
        self.user_bio_count = {}
        self.location_count = {}

        # Double Param dicts
        self.date_location_count = {}

        # List of dicts
        self.dicts = ["self.tweet_source_count", "self.hashtag_count", "self.date_count", "self.location_count", "self.user_bio_count", "self.date_location_count"]
        #self.dicts = ["self.location_count_pos", "self.location_count_neg"]
        #self.dicts = ["self.date_count"]
    def add_key_to_dict(self, dict, keys, value = 1):
        for key in keys:
            if key not in dict:
                dict[key] = 0
            dict[key] += value

    def add_key_to_2args_dict(self, dict, keys1, keys2):
        for key1 in keys1:
            for key2 in keys2:
                new_key = str(key1) + "-" + str(key2)
                if new_key not in dict:
                    dict[new_key] = 0
                dict[new_key] += 1

    def dump_dict(self, dict_str, i):
        d = eval(dict_str)
        outputfilename = self.outputfolder + self.dicts[i].split(".")[1] + ".json"
        sorted_d = dict(sorted(d.items(), key=lambda x: abs(x[1])))
        with open(outputfilename, 'w') as fp:
            json.dump(sorted_d, fp)
        print(outputfilename + " is ready.")

    def plot_dict(self, dict_str, i):
        d = eval(dict_str)
        chartname = self.chartouputfolder+'/wc_' + dict_str + '.png'
        sorted_d = dict(sorted(d.items(), key=lambda x: abs(x[1])))
        keys = [key for key, _ in sorted_d.items()][:10]
        counts = [count for _, count in sorted_d.items()][:10]
        plt.plot(keys, counts)
        plt.savefig(chartname)
        plt.show()
        plt.close()

    def plot_dict_wc(self, dict_str, i):
        d = eval(dict_str)
        chartname = 'charts/wc_' + dict_str + '.png'
        all_orgs = [(key, val) for key, val in d.items()]
        all_orgs_words = {text: freq for (text, freq) in all_orgs}
        wc = WordCloud(width=1000, height=800).generate_from_frequencies(all_orgs_words)
        plt.imshow(wc)
        plt.axis("off")
        plt.show()
        plt.imsave(chartname, wc)

    def clean_tweet_source(self, source):
        try:
            source, n = re.subn('{{(?!{)(?:(?!{{).)*?}}|<[^<]*?>', '', source, flags=re.DOTALL)
            return [source.lower()]
        except Exception as e:
            print(e)
            return []

    def clean_hashtags(self, hashtags):
        return [hashtag["text"].lower() for hashtag in hashtags]

    def clean_date(self, date_time_str, date_filters):
        # Mon Jul 18 11:54:21 +0000 2016
        try:
            date_time_obj = datetime.strptime(date_time_str, '%a %b %d %H:%M:%S +0000 %Y')
            date_as_asked = []
            for filter in date_filters:
                if filter == "year":
                    date_as_asked.append(str(date_time_obj.year))
                elif filter == "month":
                    date_as_asked.append(str(date_time_obj.month))
                elif filter == "day":
                    date_as_asked.append(str(date_time_obj.day))
                elif filter == "weekday":
                    date_as_asked.append(str(date_time_obj.strftime('%A')))
                elif filter == "hour":
                    date_as_asked.append(str(date_time_obj.hour))
                elif filter == "min":
                    date_as_asked.append(str(date_time_obj.minute))
                # print(date_as_asked)
            # year_month = [str(date_time_obj.year) + "-" + str(date_time_obj.month)]
            year_month = "-".join(date_as_asked)
            # print(year_month)
            return [year_month]
        except Exception as e:
            print(e)
            return []
        # print(date_time_obj)
        # return date_time_obj

    def clean_location(self, location):
        if location != "":
            return [location.lower()]
        return []

    def clean_location_state(self, location):
        if location != "":
            geo = location.strip().lower().split(",")
            # print(geo)
            if len(geo) < 2:
                geo = geo[0]
            elif len(geo) >= 2:
                geo = geo[-1].strip()
            return [geo]
        return []

    def clean_userbio(self, userbio):
        userbio = re.sub(r'[^a-zA-z\s]', '', userbio).lower()
        word_tokens = word_tokenize(userbio)
        word_tokens = [w for w in word_tokens if not w in self.stop_words]
        # more preprocessing here
        # print(words)
        return word_tokens

    def main(self):
        i = 0
        try:
            with open(self.inputfilename, "r") as fr:
                lines = fr.readlines()
                for line in lines:
                    try:
                        # print(line)
                        # line = line.decode('utf-8').replace('\0', '')
                        tweet = json.loads(line)
                        # print(tweet)

                        sourceExists = True if "source" in tweet else False
                        hashtagExists = True if "entities" in tweet and tweet["entities"] != None and "hashtags" in tweet["entities"] else False
                        dateExists = True if "created_at" in tweet else False
                        locationExists = True if "user" in tweet and tweet["user"] != None and "location" in tweet["user"] else False
                        userbioExists = True if "user" in tweet and tweet["user"] != None and "description" in tweet["user"] else False
                        placeExists = True if "place" in tweet and tweet["place"] != None and "full_name" in tweet["place"] else False

                        # print(tweet["full_text"])
                        snt = analyser.polarity_scores(tweet["full_text"])
                        # print(snt)
                        tweet_polarity = snt['compound']

                        # print(locationExists, placeExists, tweet_polarity)

                        # tweet source
                        if sourceExists:
                            sources = self.clean_tweet_source(tweet["source"])
                            self.add_key_to_dict(self.tweet_source_count, sources)
                        #
                        # # hashtag
                        if hashtagExists:
                            hashtags = self.clean_hashtags(tweet["entities"]["hashtags"])
                            self.add_key_to_dict(self.hashtag_count, hashtags)
                        #
                        # # date
                        if dateExists:
                             # Pass a list of parameters that you want to consider for the date in second arg
                            dates = self.clean_date(tweet["created_at"], ["year","month","day"])
                            self.add_key_to_dict(self.date_count, dates)

                        # location (of user) and place (from where the tweet is being published)
                        if locationExists:
                            # print("locationExists")
                            locations = self.clean_location(tweet["user"]["location"])
                            if tweet_polarity > 0:
                                self.add_key_to_dict(self.location_count_pos, locations, tweet_polarity)
                            else:
                                self.add_key_to_dict(self.location_count_neg, locations, tweet_polarity)

                        if placeExists:
                            # print("placeExists")
                            locations = self.clean_location_state(tweet["place"]["full_name"])
                            self.add_key_to_dict(self.location_count, locations)
                            if tweet_polarity > 0:
                                self.add_key_to_dict(self.location_count_pos, locations, tweet_polarity)
                            else:
                                self.add_key_to_dict(self.location_count_neg, locations, tweet_polarity)

                        # print(self.location_count_pos)
                        # print(self.location_count_neg)

                        # userbio
                        if userbioExists:
                            userbio = self.clean_userbio(tweet["user"]["description"])
                            self.add_key_to_dict(self.user_bio_count, userbio)
                        #
                        # # date and location
                        if dateExists and placeExists:
                            self.add_key_to_2args_dict(self.date_location_count, dates, locations)

                        if i % 10000 == 0:
                            print(i, " tweets done")

                        i += 1

                    except:
                        # print('bad json: ', line)
                        # print('bad json')
                        pass
            #pprint.pprint(self.date_count, indent=4)
            for i, dict in enumerate(self.dicts):
                self.dump_dict(dict, i)

            for i, dict in enumerate(self.dicts):
                self.plot_dict_wc(dict, i)
                
        except FileNotFoundError:
            print("unable to find tweet file")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        GetStats().main()
    except KeyboardInterrupt:
        exit(0)

