import os
from pprint import pprint
from typing import List
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
hillary_input_folder = "/media/disk/crawler/PEPr_Project_Code/speech_ir/data/2016_Data_Hillary Clinton"
donald_input_folder = "/media/disk/crawler/PEPr_Project_Code/speech_ir/data/2016_Data_Donald_Trump"
full_data_folder = "/media/disk/crawler/PEPr_Project_Code/speech_ir/data/full_data/Data/"

def read_input_folder(input_folder: str, only_ascii: bool = True) -> List[str]:
    """
    :return: a list of text, each element represents text from a file
    """
    data = []
    for filename in os.listdir(input_folder):
        with open("{}/{}".format(input_folder, filename), 'r') as fp:
            file_data = fp.read()
            if only_ascii:
                file_data = file_data.encode('ascii', errors='ignore').decode('ascii')
            data.append(file_data)
    return data

def read_full_data(only_ascii: bool = True) -> List[str]:
    data = []
    for folder in os.listdir(full_data_folder):
        with open("{}/{}/full_speech.txt".format(full_data_folder, folder), 'r') as fp:
            for spch in fp.readlines():
                data.append(spch)
    return data


def word_distribution(data: List[str]):
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