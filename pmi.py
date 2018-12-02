#!/usr/bin/env python
# coding: utf-8
import nltk
import pandas as pd
import numpy as np
from nltk.collocations import *
from nltk.corpus import stopwords
import os
import codecs

bigram_measures = nltk.collocations.BigramAssocMeasures()
#trigram_measures = nltk.collocations.TrigramAssocMeasures()

files = {}
pmi_list = {}
input_folder = '2016_Data_Hillary Clinton'
for filename in os.listdir(input_folder):
    with open("{}/{}".format(input_folder, filename), 'rb') as fp:
        files[filename] = fp.read().decode('latin-1')
    for filename,text in files.items():
        tokens = nltk.wordpunct_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        custom_stopwords = {",", "'",";" ,".",":","-","\x96","t","m","!",'"',"%","3"
                            ,"4","];","$",'â','\x80\x94', '(',"100", "33","000","/"
                            ,"11","e","[", "?","]",'."',"said","audience","yes","know"
                            ,"going","applause",'.!','u',"--","see","1","2","mean","get"
                            ,"wants","thank","across","tell","us","say","words","let"
                            ,'...[','k','12', '...','video','**[','click','\x80','\x93',')','also','10','matthews'}
        stop_words = stop_words.union(custom_stopwords)

        filtered_tokens = []
        for word in tokens:
            if word not in stop_words:
                filtered_tokens.append(word)
        finder = BigramCollocationFinder.from_words(filtered_tokens)
        finder.apply_freq_filter(3)
        pmi_list[filename] = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:10]
# pmi_list

#finding collocations words
#extract n-grams from your data and then find the ones that have the highest point wise mutual information (PMI)
#Collocations are expressions of multiple words which commonly co-occur

# finder from manually-derived FreqDists:
word_fd = nltk.FreqDist(filtered_tokens)
bigram_fd = nltk.FreqDist(nltk.bigrams(filtered_tokens))
finder = BigramCollocationFinder(word_fd, bigram_fd)
sorted(finder.nbest(bigram_measures.raw_freq, 10))

#spanning intervening words:
ignored_words = nltk.corpus.stopwords.words('english')
finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
finder.nbest(bigram_measures.likelihood_ratio, 20)

