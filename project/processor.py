from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sys
import string
import pickle
import numpy as np
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)


# ensure Python 3.x or greater sis used
if sys.version_info[0] < 3:
    raise Exception(
        "Python 3 or a more recent version is required to run this program.")

# let user know file has started running
print("Processing...")

# load data
corpus = {}
try:
    with open('data.csv', 'r', encoding='utf-8') as f:
        data = f.readlines()
        for line in data:
            datapoint = line.split(',', 2)
            corpus[datapoint[2]] = datapoint[1]
except Exception as e:
    print(e)
    print("Please make sure you have all the required files. \
    \nIf you need help, please look at the gitpage on https://github.com/canams/chatbot.")
    exit()

# standardise, tokenise, filter and stem data
processed_corpus = {}
for document in corpus:
    processed_corpus[document] = [word.lower() for word in word_tokenize(corpus[document])
                                  if not word in stopwords.words() and word.isalnum()]
    sb_stemmer = SnowballStemmer('english')
    for document in processed_corpus:
        processed_corpus[document] = [sb_stemmer.stem(
            word) for word in processed_corpus[document]]

# create vocabulary and bag of words
vocabulary = []
for document in processed_corpus:
    for word in processed_corpus[document]:
        if word not in vocabulary:
            vocabulary.append(word)

bow = {}
for document in processed_corpus:
    bow[document] = np.zeros(len(vocabulary))
    for word in processed_corpus[document]:
        index = vocabulary.index(word)
        bow[document][index] += 1

# serialise data
with open("bow.pickle", "wb") as f:
    pickle.dump(bow, f)

with open("vocabulary.pickle", "wb") as f:
    pickle.dump(vocabulary, f)

with open("corpus.pickle", "wb") as f:
    pickle.dump(corpus, f)


# let user know file completed
print("Processing Complete!")
