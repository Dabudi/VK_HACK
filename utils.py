from pymorphy2 import MorphAnalyzer
import re
import nltk
import numpy as np

MODEL_DIMS = 300

try:
    stop_words = nltk.corpus.stopwords.words('russian')
except:
    nltk.download('stopwords')
    stop_words = nltk.corpus.stopwords.words('russian')
stop_words.extend(['порт', 'севкабель'])


def preprocessing(text):
    text = re.sub('[^0-9a-zа-я ]', '', text.lower())
    m = MorphAnalyzer()
    text = [x for x in text.split() if x not in stop_words]
    processed = ' '.join(list(map(lambda x: m.parse(x)[0].normal_form, text)))
    return processed

def vectorize(model, text):
    if text is None:
        text = ''
    text = preprocessing(text).split()
    vector = np.mean((list(map(lambda x: get_vector(model=model, word=x), text))), axis=0)
    try:
        vector[0]
        return vector
    except:
        return np.zeros(MODEL_DIMS)

def get_vector(model, word):
    try:
        return model.wv.get_vector(word)
    except:
        return np.zeros(MODEL_DIMS)
