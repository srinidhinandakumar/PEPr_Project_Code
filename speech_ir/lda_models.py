from gensim import models, corpora

from speech_ir.visualizer import read_input_folder
from speech_ir.speech_sanitizer import speech_sanitizer

num_topics = 4

def build_lda_model(num_topics: int = num_topics, passes: int = 50):
    data = read_input_folder()
    doc_clean = [speech_sanitizer(doc).split() for doc in data]

    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    lda_model = models.ldamodel.LdaModel(doc_term_matrix, id2word=dictionary,
                                         num_topics=num_topics, passes=passes)
    return lda_model, dictionary


def predict_topics(tweet: str, lda_model, corpora_dict):
    pred = regress_topics(tweet, lda_model, corpora_dict)
    return max(pred, key=pred.get)


def regress_topics(tweet: str, lda_model, corpora_dict):
    test_words = speech_sanitizer(tweet)
    test_vec = corpora_dict.doc2bow(test_words.split())
    return dict(lda_model[test_vec])

