from gensim import models, corpora

from speech_ir.visualizer import read_input_folder
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string


def lda_model():
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    data = read_input_folder()
    doc_clean = [clean(doc).split() for doc in data]

    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    ldamodel = models.ldamodel.LdaModel(doc_term_matrix,id2word=dictionary, num_topics=3, passes=50)

    for idx, topic in ldamodel.print_topics():
        print(idx, topic)

    return ldamodel


if __name__ == '__main__':
    lda_model()

