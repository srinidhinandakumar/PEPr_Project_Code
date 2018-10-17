from collections import defaultdict

from spacy.lang.en import English
from wordcloud import WordCloud
from speech_ir.visualizer import read_input_folder
import spacy
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List
from spacy.lang.en.stop_words import STOP_WORDS


"""
todo: 
use tf-idf to plot wordclouds
wordcloud for pronouns, verbs etc...
"""
nlp: English = spacy.load('en_core_web_sm')


def pos_tags_wc(docs):
    pos_tags = defaultdict(int)
    for doc in docs:
        for token in doc:
            if not nlp.vocab[token.text].is_stop:
                pos_tags[(token.text, token.pos_)] += 1

    all_nouns = [(key, val) for key, val in pos_tags.items() if key[1] == "NOUN"]
    all_nouns.sort(key = lambda x: x[1], reverse=True)
    all_noun_words = {text:freq for ((text, _),freq) in all_nouns}
    wc = WordCloud(width=1000, height=800).generate_from_frequencies(all_noun_words)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    plt.imsave("data/images/pos_nouns_freq.png", wc)

def ner_tags_wc(docs):
    ner_tags = defaultdict(int)
    for doc in docs:
        for token in doc.ents:
            if not nlp.vocab[token.text].is_stop:
                ner_tags[(token.text, token.label_)] += 1
    all_orgs = [(key, val) for key, val in ner_tags.items() if key[1] == "ORG"]
    all_orgs_words = {text:freq for ((text, _), freq) in all_orgs}
    wc = WordCloud(width=1000, height=800).generate_from_frequencies(all_orgs_words)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    plt.imsave("data/images/org_freq.png", wc)

    all_persons = [(key, val) for key, val in ner_tags.items() if key[1] == "PERSON"]
    all_person_words = {text: freq for ((text, _), freq) in all_persons}
    wc = WordCloud(width=1000, height=800).generate_from_frequencies(all_person_words)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    plt.imsave("data/images/person_freq.png", wc)


def tf_idf(docs):
    # Removing stop words from the corpus
    stop_words = set(stopwords.words('english'))
    filtered_data = [' '.join([word for word in word_tokenize(page) if word not in stop_words]) for page in docs]

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

data = read_input_folder()
docs = [nlp(text) for text in data]
ner_tags_wc(docs)