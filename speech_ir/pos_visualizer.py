from collections import defaultdict
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt
import spacy
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en import English
from wordcloud import WordCloud

from speech_ir.visualizer import read_input_folder, read_full_data, \
    hillary_input_folder, donald_input_folder

"""
todo: 
use tf-idf to plot wordclouds
"""


custom_stopwords = {"time", "years", "lot", "country", "countries",
                    "people", "applause", "things", "way", "lot", "world",
                    "kind", "percent", "democrats", "republicans", "americans",
                    "america", "president", "today", "program", "what", "men"}


nlp: English = spacy.load('en_core_web_sm')


def pos_tags_wc(docs):
    pos_tags = defaultdict(int)
    for doc in docs:
        for token in doc:
            if nlp.vocab[token.text].is_stop or token.text.lower() in custom_stopwords:
                continue
            pos_tags[(token.text, token.pos_)] += 1

    # print(pos_tags)
    all_tags = {tag for (_, tag) in pos_tags}
    for tag in all_tags:
        tag_words = filter_tags(pos_tags, tag)
        if tag_words:
            build_wc_from_dict(tag_words, "pos_" + tag)


def ner_tags_wc(docs):
    ner_tags: Dict[Tuple[str, str], int] = defaultdict(int)
    for doc in docs:
        for token in doc.ents:
            if nlp.vocab[token.text].is_stop or token.text.lower() in custom_stopwords:
                continue
            ner_tags[(token.text, token.label_)] += 1

    # print(ner_tags)

    all_tags: List[str] = {tag for (_, tag) in ner_tags}
    for tag in all_tags:
        tag_words: Dict[str, int] = filter_tags(ner_tags, tag)
        if tag_words:
            build_wc_from_dict(tag_words, "ner_" + tag)


def filter_tags(d: Dict[Tuple[str, str], int], filter_tag: str) -> Dict[
    str, int]:
    return {text: freq for (text, tag), freq in d.items() if tag == filter_tag}


def build_wc_from_dict(info: Dict[str, int], name):
    wc = WordCloud(width=1000, height=800).generate_from_frequencies(info)
    # plt.imshow(wc)
    plt.axis("off")
    plt.show()
    plt.imsave("data/images/{}.png".format(name), wc)

def tf_idf(docs):
    # Removing stop words from the corpus
    stop_words = set(stopwords.words('english'))
    filtered_data = [' '.join([word for word in word_tokenize(page) if word.lower()
                               not in stop_words]) for page in docs]

    # Generating tfidf values
    tfidf_values = defaultdict(int)
    tf = TfidfVectorizer()
    tf_matrix = tf.fit_transform(filtered_data)

    # Aggregating the tdidf values all over the corpus
    feature_names = tf.get_feature_names()
    for doc in range(len(filtered_data)):
        feature_index = tf_matrix[doc, :].nonzero()[1]
        for index in feature_index:
            tfidf_values[feature_names[index]] += tf_matrix[doc, index]


    wc = WordCloud(width=1000, height=800).generate_from_frequencies(tfidf_values)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    plt.imsave("data/images/freq.png", wc)



data =  read_full_data()
docs = [nlp(text) for text in data]
ner_tags_wc(docs)
pos_tags_wc(docs)



