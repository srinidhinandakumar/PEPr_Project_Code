#!/usr/bin/env python
# coding: utf-8

import nltk
from nltk.collocations import *
from nltk.corpus import stopwords

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()


data = []
input_folder = 'Trump_data'
filename = 'speech_00.txt'
with open("{}/{}".format(input_folder, filename), 'r') as fp:
    data.append(fp.read())
data
text = ''.join(data)
tokens = nltk.wordpunct_tokenize(text)

finder = BigramCollocationFinder.from_words(tokens)

finder.apply_freq_filter(2) 

#finding collocations words
#extract n-grams from your data and then find the ones that have the highest point wise mutual information (PMI)
#Collocations are expressions of multiple words which commonly co-occur
finder.nbest(bigram_measures.pmi, 20) 

#spanning intervening words:
ignored_words = nltk.corpus.stopwords.words('english')
finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
finder.nbest(bigram_measures.likelihood_ratio, 20)
