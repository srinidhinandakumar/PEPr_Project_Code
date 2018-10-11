import nltk
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

finder = BigramCollocationFinder.from_words(
   nltk.corpus.genesis.words('english-web.txt'))

finder.apply_freq_filter(3) 

finder.nbest(bigram_measures.pmi, 10)  

