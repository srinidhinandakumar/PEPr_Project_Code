import nltk
from nltk.corpus import stopwords
import string

def file_reading(input_folder,filename):
    data = []
    with open("{}/{}".format(input_folder, filename), 'r') as fp:
        data.append(fp.read())
    data
    text = ''.join(data).lower()
    tokens = nltk.wordpunct_tokenize(text)
    return tokens

def cleaning_data(tokens):
    stop = stopwords.words('english') + list(string.punctuation)
    clean_data = [i for i in tokens if i not in stop]
    return clean_data


# here, for work_features we need to use the features that we found from winning candidates speech
# I used Trump's speech_00.txt file to extract features (most common words used by that candiates)

file_data = file_reading('Trump_data','speech_00.txt')
clean_data = cleaning_data(file_data)

data_freq = nltk.FreqDist(clean_data)
word_features = list(data_freq.keys())[:30]
word_features


#Now, we can use this features list to find out feature presence in the new speech. It will be boolean
def find_features(document):
    features = {}
    for w in word_features:
        features[w] = (w in document)
    return features

#using Clinton's speech(test data) to see wheather whose features(from Trump's speech) are present in her speech or not
test_file_data = file_reading('Clinton_data','speech_13.txt')
test_clean_data = cleaning_data(test_file_data)
test_file_data
print(find_features(test_clean_data))

