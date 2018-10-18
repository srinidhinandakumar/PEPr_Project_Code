from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.toktok import ToktokTokenizer
tokenizer = ToktokTokenizer()
import string

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
stemmer = PorterStemmer()

custom_stopwords = {"going", "applause","right", "you", "the", "were", "said",
                    "theyr", "it", "want", "also", "new", "one", "say", "get"}
stop = stop.union(custom_stopwords)


def speech_sanitizer(doc: str, lemmatize: bool = True):
    """
    using this method particularly for speech data, use tweet_sanitizer methods
    if you are working with twitter data
    :param doc: entire document's string representation
    :return:
    """
    tokens = tokenizer.tokenize(doc)
    tokens = [token.strip() for token in tokens]
    stop_free = [token for token in tokens if token.lower() not in stop]
    stop_free = ' '.join(stop_free)
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    if lemmatize:
        return " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return punc_free
