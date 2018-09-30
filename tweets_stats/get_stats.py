import json
import matplotlib.pyplot as plt
import re

from datetime import datetime

class GetStats:
    def __init__(self):
        # self.inputfilename = "../twitter_scraper/data/alltweets.json"
        self.inputfilename = "../twitter_scraper/data/kdata.json"
        self.outputfolder = "stats/"

        # Single Param dicts
        self.tweet_source_count = {}
        self.hashtag_count = {}
        self.date_count = {}
        self.location_count = {}

        # Double Param dicts
        self.date_location_count = {}

        # List of dicts
        self.dicts = ["self.tweet_source_count", "self.hashtag_count", "self.date_count", "self.location_count", "self.date_location_count"]

    def add_key_to_dict(self, dict, keys):
        for key in keys:
            if key not in dict:
                dict[key] = 0
            dict[key] += 1

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
        sorted_d = dict(sorted(d.items(), key=lambda x: -x[1]))
        with open(outputfilename, 'w') as fp:
            json.dump(sorted_d, fp)
        print(outputfilename + " is ready.")

    def plot_dict(self, dict_str, i):
        d = eval(dict_str)
        chartname = 'charts/' + dict_str + '.png'
        sorted_d = dict(sorted(d.items(), key=lambda x: -x[1]))
        keys, counts = [], []
        i = 0
        for key, val in sorted_d.items():
            if i > 10:
                break
            keys.append(key)
            counts.append(val)
            i += 1
        plt.plot(keys, counts)
        plt.savefig(chartname)
        plt.show()
        plt.close()

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

    def main(self):
        try:
            with open(self.inputfilename, "r") as fr:
                lines = fr.readlines()
                for line in lines:
                    tweet = json.loads(line)

                    sourceExists = True if "source" in tweet else False
                    hashtagExists = True if "entities" in tweet and tweet["entities"] != None and "hashtags" in tweet["entities"] else False
                    dateExists = True if "created_at" in tweet else False
                    locationExists = True if "user" in tweet and tweet["user"] != None and "location" in tweet["user"] else False
                    placeExists = True if "place" in tweet and tweet["place"] != None and "full_name" in tweet["place"] else False

                    # tweet source
                    if sourceExists:
                        sources = self.clean_tweet_source(tweet["source"])
                        self.add_key_to_dict(self.tweet_source_count, sources)

                    # hashtag
                    if hashtagExists:
                        hashtags = self.clean_hashtags(tweet["entities"]["hashtags"])
                        self.add_key_to_dict(self.hashtag_count, hashtags)

                    # date
                    if dateExists:
                        # Pass a list of parameters that you want to consider for the date in second arg
                        dates = self.clean_date(tweet["created_at"], ["hour"])
                        self.add_key_to_dict(self.date_count, dates)

                    # location (of user) and place (from where the tweet is being published)
                    if locationExists:
                        locations = self.clean_location(tweet["user"]["location"])
                        self.add_key_to_dict(self.location_count, locations)
                    if placeExists:
                        locations = self.clean_location(tweet["place"]["full_name"])
                        self.add_key_to_dict(self.location_count, locations)

                    # date and location
                    if dateExists and locationExists:
                        self.add_key_to_2args_dict(self.date_location_count, dates, locations)


            for i, dict in enumerate(self.dicts):
                self.dump_dict(dict, i)

            for i, dict in enumerate(self.dicts):
                self.plot_dict(dict, i)

        except FileNotFoundError:
            print("unable to find tweet file")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        GetStats().main()
    except KeyboardInterrupt:
        exit(0)

