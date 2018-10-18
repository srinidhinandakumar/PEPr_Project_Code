import os
from pprint import pprint
from typing import List
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from sklearn.feature_extraction.text import CountVectorizer
input_folder = "Trump_data"


def read_input_folder():
    """
    :return: a list of text, each element represents text from a file
    """
    data = []
    for filename in os.listdir(input_folder):
        with open("{}/{}".format(input_folder, filename), 'r') as fp:
            data.append(fp.read())
    return data



def remove_stopwords(data, is_lower_case=False):
    stopword_list = nltk.corpus.stopwords.words('english')
    tokenizer = ToktokTokenizer()
    tokens = tokenizer.tokenize(data)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text


def bar_viz(words,frequency):

    plt.xlabel('Top 10 words')
    plt.ylabel('Word frequency')
    indexes = np.arange(len(words) )
    width = 0.2
    plt.bar(indexes, frequency, width)
    plt.xticks(indexes + width * .4, words)
    plt.tight_layout()

    plt.show()


def word_distribution(data: List[str]):
    print(data)
    no_stop_data = remove_stopwords(data)
    no_stop_data = [no_stop_data]
    counter = CountVectorizer()
    counter.fit(no_stop_data)
    # word_counts list of key val with [(word,count)]
    word_counts = list(counter.vocabulary_.items())
    
    word_counts.sort(key = lambda x:x[1], reverse=True)
    # print(word_counts)

    #words is list of top 10 words
    words = [word for word, _ in word_counts][:20]
    
    frequency = [freq for _, freq in word_counts][:20]

    # plt.plot(words, frequency)
    # plt.bar(words,frequency)
    # plt.show()
    bar_viz(words,frequency)
    
    
# def tfidf_distribution()


if __name__ == '__main__':
    word_distribution(read_input_folder())