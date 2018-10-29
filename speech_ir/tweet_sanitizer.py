import json
import string
import unicodedata

import spacy

nlp = spacy.load('en', parse=True, tag=True, entity=True)
import re

import nltk
from nltk.tokenize.toktok import ToktokTokenizer

import sys, os


tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')
twitter_replace_file = "../../speech_ir/data/twitter_replace.json"

with open(twitter_replace_file, 'r') as fp:
    twitter_shorthand_notations = json.load(fp)


def strip_links(text):
    link_regex = re.compile(
        '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?+-=\\\.&](#!)?)*)',
        re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text


def strip_all_entities(text):
    entity_prefixes = ['@', '#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode(
        'utf-8', 'ignore')
    return text


def simple_stemmer(text):
    ps = nltk.porter.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text


def lemmatize_text(text):
    text = nlp(text)
    text = ' '.join(
        [word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in
         text])
    return text


def expandContractions(text):
    c_re = re.compile('(%s)' % '|'.join(twitter_shorthand_notations.keys()))

    def replace(match):
        return twitter_shorthand_notations[match.group(0)]

    text = c_re.sub(replace, text.lower())
    return text


def strip_mentions(text):
    entity_prefixes = ['@']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def strip_hashtags(text):
    entity_prefixes = ['#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)

    # trying to remove RT symbol form tweet
    tweet = ' '.join(words)
    if tweet.lower().startswith("rt"):
        return tweet[2:].strip()
    return tweet


def remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if
                           token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if
                           token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def tweet_sanitize(tweet: str) -> str:
    """
    removes the noise in tweet, doesn't remove stopwords or perform stemming
    :param tweet:
    :return:
    """
    pipeline = [strip_links, strip_mentions, strip_hashtags, strip_all_entities,
                remove_special_characters]
    for fun in pipeline:
        tweet = fun(tweet)
    return tweet


def tweet_stemmer(tweet: str, is_lower: bool = True) -> str:
    """
    removes the noise in tweet along with removing stopwords and stemming
    :param tweet:
    :return:
    """
    tweet = tweet_sanitize(tweet)
    tweet = remove_stopwords(tweet, is_lower)
    return simple_stemmer(tweet)
