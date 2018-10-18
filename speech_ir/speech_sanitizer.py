from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
stemmer = PorterStemmer()


def speech_sanitizer(doc: str):
    """
    using this method particularly for speech data, use tweet_sanitizer methods
    if you are working with twitter data
    :param doc: entire document's string representation
    :return:
    """
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    # normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    normalized = " ".join(stemmer.stem(word) for word in punc_free.split())
    return normalized

