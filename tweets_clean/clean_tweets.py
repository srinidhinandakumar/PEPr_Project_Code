import re
import json
from textblob import TextBlob
import string

# inputfilename = "../twitter_scraper/data/alltweets.json"
# outputfilename = "tweets_clean/cleaned_data/alltweets.json"
expansions = "tweets_clean/expansions.json" # update relative path if running this file alone


with open(expansions, "r") as fp:
    cList = json.load(fp)
c_re = re.compile('(%s)' % '|'.join(cList.keys()))


def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text


def expandContractions(text):
    global c_re

    def replace(match):
        return cList[match.group(0)]

    text = c_re.sub(replace, text.lower())
    return text


def strip_hashtags(text):

    entity_prefixes = ['#','@']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] != "#":
                words.append(word)
    return ' '.join(words)


def strip_mentions(text):
    entity_prefixes = ['@','#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] != "@":
                words.append(word)
    return ' '.join(words)


def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def spell_check(text):
    b = TextBlob(text)
    correct_spelling = b.correct()
    return correct_spelling


def cleaning_pipeline(text):
    text = expandContractions(text)
    text = strip_links(text)
    text = strip_mentions(text)
    text = strip_hashtags(text)
    text = spell_check(text)
    #text = remove_special_characters(text)

    return str(text)
