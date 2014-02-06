from nltk.corpus import movie_reviews
import nltk
import random
from numpy import array, empty, ones, nonzero, repeat, zeros
import numpy

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

documents = [(list(movie_reviews.words(fileid)), category)
		for category in movie_reviews.categories()
		for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)
