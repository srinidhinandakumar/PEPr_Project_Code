import numpy as np
from corextopic import corextopic as ct
from speech_ir.visualizer import read_full_data
import scipy.sparse as ss
from sklearn.feature_extraction.text import CountVectorizer

data = read_full_data()


countV = CountVectorizer()
countV.fit(data)
vocab = list(countV.vocabulary_)

# print(vocab)
print(len(vocab))
l = len(vocab)
matrix = []
for doc in data:
    cur = [0]*l
    doc_count = CountVectorizer()
    doc_count.fit([doc])
    doc_vocab = doc_count.vocabulary_
    for word in doc_vocab:
        cur[vocab.index(word)] = 1
    matrix.append(cur)


matrix = np.array(matrix, dtype=int)
matrix = ss.csc_matrix(matrix)

anchors_words = [
     ["people", "know", "country", "Trump", "great", "like", "Hillary", "Clinton"],
     ["world", "isis", "iraq", "terrorist", "war", "israel", "saudi", "oil"],
     ["job", "jobs", "people", "money"]
    ]



anchors_words = []


model = ct.Corex(n_hidden=3)
model.fit(matrix, words=vocab, docs=data, anchors=anchors_words)

# print(model.get_topics())

for topic in model.get_topics():
    topic_words = []
    for word,_ in topic:
        topic_words.append(word)
    print(topic_words)


#
# print(doc_clean)
#
#
# words = ['trade', 'market', 'money', 'market', 'china']
#
# model = ct.Corex(n_hidden=2)
# model.fit(doc_clean, words=words)
# print(model.get_topics())