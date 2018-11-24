from gensim import models, corpora

from speech_ir.visualizer import read_input_folder, read_full_data
from speech_ir.speech_sanitizer import speech_sanitizer


def build_lda_model(num_topics: int = 3, passes: int = 50):
    data = read_full_data()
    doc_clean = [speech_sanitizer(doc).split() for doc in data]
    # print(doc_clean)
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    lda_model = models.ldamodel.LdaModel(doc_term_matrix, id2word=dictionary,
                                         num_topics=num_topics, passes=passes,
                                         random_state=4)
    return lda_model, dictionary


def predict_topics(tweet: str, lda_model, corpora_dict):
    pred = regress_topics(tweet, lda_model, corpora_dict)
    return max(pred, key=pred.get)

def regress_topics(tweet: str, lda_model, corpora_dict):
    test_words = speech_sanitizer(tweet)
    test_vec = corpora_dict.doc2bow(test_words.split())
    return dict(lda_model[test_vec])


if __name__ == '__main__':
    lda_model, lda_dict = build_lda_model()
    print(lda_model.print_topics())