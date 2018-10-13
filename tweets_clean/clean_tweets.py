import re
import json
from textblob import TextBlob
import string

class CleanTweet:
    def __init__(self):
        self.inputfilename = "../twitter_scraper/data/alltweets.json"
        self.outputfilename = "cleaned_data/alltweets.json"

        self.cList = {
          "ain't": "am not",
          "aren't": "are not",
          "can't": "cannot",
          "can't've": "cannot have",
          "'cause": "because",
          "could've": "could have",
          "couldn't": "could not",
          "couldn't've": "could not have",
          "didn't": "did not",
          "doesn't": "does not",
          "don't": "do not",
          "hadn't": "had not",
          "hadn't've": "had not have",
          "hasn't": "has not",
          "haven't": "have not",
          "he'd": "he would",
          "he'd've": "he would have",
          "he'll": "he will",
          "he'll've": "he will have",
          "he's": "he is",
          "how'd": "how did",
          "how'd'y": "how do you",
          "how'll": "how will",
          "how's": "how is",
          "I'd": "I would",
          "I'd've": "I would have",
          "I'll": "I will",
          "I'll've": "I will have",
          "I'm": "I am",
          "I've": "I have",
          "isn't": "is not",
          "it'd": "it had",
          "it'd've": "it would have",
          "it'll": "it will",
          "it'll've": "it will have",
          "it's": "it is",
          "let's": "let us",
          "ma'am": "madam",
          "mayn't": "may not",
          "might've": "might have",
          "mightn't": "might not",
          "mightn't've": "might not have",
          "must've": "must have",
          "mustn't": "must not",
          "mustn't've": "must not have",
          "needn't": "need not",
          "needn't've": "need not have",
          "o'clock": "of the clock",
          "oughtn't": "ought not",
          "oughtn't've": "ought not have",
          "shan't": "shall not",
          "sha'n't": "shall not",
          "shan't've": "shall not have",
          "she'd": "she would",
          "she'd've": "she would have",
          "she'll": "she will",
          "she'll've": "she will have",
          "she's": "she is",
          "should've": "should have",
          "shouldn't": "should not",
          "shouldn't've": "should not have",
          "so've": "so have",
          "so's": "so is",
          "that'd": "that would",
          "that'd've": "that would have",
          "that's": "that is",
          "there'd": "there had",
          "there'd've": "there would have",
          "there's": "there is",
          "they'd": "they would",
          "they'd've": "they would have",
          "they'll": "they will",
          "they'll've": "they will have",
          "they're": "they are",
          "they've": "they have",
          "to've": "to have",
          "wasn't": "was not",
          "we'd": "we had",
          "we'd've": "we would have",
          "we'll": "we will",
          "we'll've": "we will have",
          "we're": "we are",
          "we've": "we have",
          "weren't": "were not",
          "what'll": "what will",
          "what'll've": "what will have",
          "what're": "what are",
          "what's": "what is",
          "what've": "what have",
          "when's": "when is",
          "when've": "when have",
          "where'd": "where did",
          "where's": "where is",
          "where've": "where have",
          "who'll": "who will",
          "who'll've": "who will have",
          "who's": "who is",
          "who've": "who have",
          "why's": "why is",
          "why've": "why have",
          "will've": "will have",
          "won't": "will not",
          "won't've": "will not have",
          "would've": "would have",
          "wouldn't": "would not",
          "wouldn't've": "would not have",
          "y'all": "you all",
          "y'alls": "you alls",
          "y'all'd": "you all would",
          "y'all'd've": "you all would have",
          "y'all're": "you all are",
          "y'all've": "you all have",
          "you'd": "you had",
          "you'd've": "you would have",
          "you'll": "youyou will",
          "you'll've": "you will have",
          "you're": "you are",
          "you've": "you have"
        }

        self.c_re = re.compile('(%s)' % '|'.join(self.cList.keys()))


        
    def strip_links(self, text):
        link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links         = re.findall(link_regex, text)
        for link in links:
            text = text.replace(link[0], ', ')    
        return text
    
    def expandContractions(self, text):
        c_re=self.c_re
        def replace(match):
            return cList[match.group(0)]
        
        text = c_re.sub(replace, text.lower())
        return text

    def strip_hashtags(self, text):
        entity_prefixes = ['#']
        for separator in  string.punctuation:
            if separator not in entity_prefixes :
                text = text.replace(separator,' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        return ' '.join(words)
    
    def strip_mentions(self, text):
        entity_prefixes = ['@']
        for separator in  string.punctuation:
            if separator not in entity_prefixes :
                text = text.replace(separator,' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        return ' '.join(words)
    
    def remove_special_characters(self, text, remove_digits=False):
        pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
        text = re.sub(pattern, '', text)
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return text
    
    def spellcheck(self, text):
        b = TextBlob(text)
        correct_spelling = b.correct()
        return correct_spelling

    def cleaning_pipeline(self, text):
        text = self.spellcheck(text)
        #text = self.remove_special_characters(text)
        #print("1")
        text = self.strip_mentions(text)
        text = self.strip_hashtags(text)
        text = self.expandContractions(text)
        text = self.strip_links(text)
        
        return text

    def main(self):
        try:
            result = ""
            count=0
            allc = 0
            with open(self.inputfilename, "r") as fr:
                lines = fr.readlines()
                for line in lines:
                    tweet = json.loads(line)
                    print(tweet["id"])
                    cleaned_tweet = self.cleaning_pipeline(tweet["full_text"])
                    tweet["full_text"] = cleaned_tweet
                    result+=str(tweet)+"\n"
                    count+=1
                    if count==800:
                        allc+=count
                        print("*****Cleaned ",allc," tweets*****")
                        with open(self.outputfilename, "a") as fq:
                            fq.write(result)
                        result=""
                        count=0
            # write into output folder and file
            print(result)
            with open(self.outputfilename, "a") as fq:
                fq.write(result)
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

