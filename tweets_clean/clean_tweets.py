import json

class CleanTweet:
    def __init__(self):
        self.inputfilename = "../twitter_scraper/data/alltweets.json"
        self.outputfolder = "cleaned_data/alltweets.json"

    def spellcheck(self, text):
        return text

    def cleaning_pipeline(self, text):
        text = self.spellcheck(text)
        return text

    def main(self):
        try:
            with open(self.inputfilename, "r") as fr:
                lines = fr.readlines()
                for line in lines:
                    tweet = json.loads(line)
                    cleaned_tweet = self.cleaning_pipeline(tweet["full_text"])
                    tweet["full_text"] = cleaned_tweet
                # write into output folder and file
                # may be we'll use this file for predicting polarity and topic modelling

        except FileNotFoundError:
            print("unable to find tweet file")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        CleanTweet().main()
    except KeyboardInterrupt:
        exit(0)

