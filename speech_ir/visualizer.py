import os
from pprint import pprint
from typing import List
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

input_folder = "/Users/srinidhi/Desktop/all-twitter-files/2016_Data_Donald_Trump"


def read_input_folder():
    """
    :return: a list of text, each element represents text from a file
    """
    data = []
    for filename in os.listdir(input_folder):
        if filename == "Donald Trump_September 24, 2016.txt":  # update as necessary
            with open("{}/{}".format(input_folder, filename), 'r') as fp:
                data.append(fp.read())
            return data


def word_distribution(data):
    counter = CountVectorizer()
    counter.fit(data)
    word_counts = list(counter.vocabulary_.items())
    word_counts.sort(key = lambda x:x[1], reverse=True)
    words = [word for word, _ in word_counts][:10]
    frequency = [freq for _, freq in word_counts][:10]
    plt.plot(words, frequency)
    plt.show()


if __name__ == '__main__':
    word_distribution(read_input_folder())