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


def speech_sanitizer(doc: str):
    """
    using this method particularly for speech data, use tweet_sanitizer methods
    if you are working with twitter data
    :param doc: entire document's string representation
    :return:
    """
    
#   stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
#removing stop_words
    tokens = tokenizer.tokenize(doc)
    is_lower_case = False
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        stop_free = [token for token in tokens if token not in stop]
    else:
        stop_free = [token for token in tokens if token.lower() not in stop]
    stop_free = ' '.join(stop_free)
    
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    # normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    normalized = " ".join(stemmer.stem(word) for word in punc_free.split())
    return normalized

