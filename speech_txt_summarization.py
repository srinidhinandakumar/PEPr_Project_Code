# source: https://stackabuse.com/text-summarization-with-nltk-in-python/
import bs4 as bs  
import urllib.request  
import re
import nltk

data = '2016_Data_Donald_Trump/Donald Trump_September 24, 2016.txt'
text = ""

fp = open(data,"r")
for line in fp:
	text += line

#prepocessing - Removing Square Brackets and Extra Spaces
text = re.sub(r'\[[0-9]*\]', ' ', text)  
text = re.sub(r'\s+', ' ', text) 
# Removing special characters and digits
formated_text = re.sub('[^a-zA-Z]', ' ', text )  
formated_text = re.sub(r'\s+', ' ', formated_text)  

#Converting Text To tokens
sentence_list = nltk.sent_tokenize(text)  

#findind weighted freq of occurance
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}  
for word in nltk.word_tokenize(formated_text):  
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():  
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

print(sentence_list)
sentence_scores = {}  
for sent in sentence_list:  
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

#Getting summary
import heapq  
print(sentence_scores)
summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)  
print(summary)  
