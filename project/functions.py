import numpy as np
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import en_core_web_sm
import textdistance
import time
import re
import pickle

nlp = en_core_web_sm.load()
np.seterr(divide='ignore', invalid='ignore')

def printError(e):
    print(e)
    print("Please make sure you have run processor.py first. \
    \nIf you need help, please look at the gitpage on https://github.com/canams/chatbot.")

try:
    with open("bow.pickle", "rb") as f:
        bow = pickle.load(f)
except Exception as e:
    printError(e)
    exit()

try:
    with open("vocabulary.pickle", "rb") as f:
        vocab = pickle.load(f)
except Exception as e:
    printError(e)
    exit()

try:
    with open("corpus.pickle", "rb") as f:
        corpus = pickle.load(f)
except Exception as e:
    printError(e)
    exit()


def process_input(text, vocab):
    #tokenise
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text)

    #remove stop words 
    filtered = []
    for token in tokens:
        if token not in stopwords.words():
            filtered.append(token.lower())
    
    #stem
    sb_stemmer = SnowballStemmer('english')
    processed = []
    for word in filtered:
        processed.append(sb_stemmer.stem(word))

    #bow model
    bow = np.zeros(len(vocab))
    for word in processed:
        if word in vocab:
            index = vocab.index(word)
            bow[index] += 1

    return bow

def square_rooted(x):
   return round(sqrt(sum([a*a for a in x])),3)
  
def similarity(v1, v2):
    sim= 1 - (np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))
    return sim

def set_name(text):
    if text == "stop":
        return "STOP"
    name = ""
    if len(text.split()) == 1:
        name = text.capitalize()
    doc = nlp(text)
    for X in doc.ents:
        if X.label_ == 'PERSON':
            name = X.text.capitalize()
    
    return name

def name_intent(text):
    phrases = ["call me", "change my name", "can you call me"]
    for phrase in phrases:
        if textdistance.jaccard(phrase.split(), text.split()) >= 0.5:
            return True

    return False

def small_talk_intent(text):
    text = re.sub(r'[^\w\s]', '', text).lower() 
    mood_phrases = ["how are you", "how is it going", "hows it going", 
    "how you are", "whats up", "hows your day", "how your day"]
    greeting_phrases = ["hello", "hi", "hey", "hiya", "good morning", 
    "good evening", "good afternoon"]
    general_phrases = ["anything", "random", "whatever", "idk", "i dont know", 
    "idm", "i dont mind", "everything", "general"]
    name_phrases =  ["what is my name", "whats my name", "who am i", "what am i called"]

    for phrase in mood_phrases:
        if textdistance.jaccard(phrase.split(), text.lower().split()) >= 0.5:
            return "mood"

    for phrase in greeting_phrases:
        if textdistance.jaccard(phrase.split(), text.lower().split()) >= 0.5:
            return "greetings"
    
    for phrase in general_phrases:
        if textdistance.jaccard(phrase.split(), text.lower().split()) >= 0.5:
            return "general"


    for phrase in name_phrases:
        if textdistance.jaccard(phrase.split(), text.lower().split()) >= 0.5:
            return "name"

    return ""


def question_intent(text):
    question_words = ["what", "who", "when", "how", "why", "which", "where", "whom", "whose"]
    if text.split()[0].lower() in question_words:
        return True
    return False

def process_question(text):
        #process search term
        search_bow = process_input(text, vocab)
        min_distance = float('inf')
        relevant_doc = []
        for document in bow:
            distance = similarity(search_bow, bow[document])
            if distance < min_distance:
                min_distance = distance
                relevant_doc = document
        if min_distance >= 0.45:
            time.sleep(1)
            print("Sorry, I'm not able to answer that yet.")
        else:
            time.sleep(1)
            print(relevant_doc)

