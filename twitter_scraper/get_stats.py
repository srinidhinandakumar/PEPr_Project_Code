import json
import re

class GetStats:
    def __init__(self):
        self.inputfilename = "data/alltweets.json"
        self.outputfolder = "stats/"
        self.tweet_source_count = {}
        self.hashtag_count = {}
        self.dicts = ["self.tweet_source_count", "self.hashtag_count"]

    def add_key_to_dict(self, dict, keys):
        for key in keys:
            if key not in dict:
                dict[key] = 0
            dict[key] += 1

    def dump_dict(self, dict, i):
        outputfilename = self.outputfolder + self.dicts[i] + ".json"
        with open(outputfilename, 'w') as fp:
            json.dump(eval(dict), fp)
        print(outputfilename + " is ready.")

    def clean_tweet_source(self, source):
        source, n = re.subn('{{(?!{)(?:(?!{{).)*?}}|<[^<]*?>', '', source, flags=re.DOTALL)
        # print(source)
        return [source]

    def clean_hashtags(self, hashtags):
        return [hashtag["text"] for hashtag in hashtags]

    def main(self):
        try:
            with open(self.inputfilename, "r") as fr:
                lines = fr.readlines()
                for line in lines:
                    tweet = json.loads(line)

                    # tweet source
                    sources = self.clean_tweet_source(tweet["source"])
                    self.add_key_to_dict(self.tweet_source_count, sources)

                    # hashtag
                    hashtags = self.clean_hashtags(tweet["entities"]["hashtags"])
                    self.add_key_to_dict(self.hashtag_count, hashtags)

            for i, dict in enumerate(self.dicts):
                self.dump_dict(dict, i)

        except FileNotFoundError:
            print("unable to find tweet file")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    try:
        GetStats().main()
    except KeyboardInterrupt:
        exit(0)

