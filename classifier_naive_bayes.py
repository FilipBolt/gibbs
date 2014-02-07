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

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = all_words.keys()[:2000]

featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)

vocabulary_size = 500

most_informative = classifier.most_informative_features(vocabulary_size)

vocabulary_words = []
for feature, flag in most_informative:
	feature = feature.replace('contains', '')
	feature = feature.replace('(','')
	feature = feature.replace(')','')
	vocabulary_words.append(feature)

print vocabulary_words

freq_dict = dict.fromkeys(vocabulary_words,0)

document_num = 10
i = 0
true_labels = empty(document_num, int)
corpus = empty((document_num, vocabulary_size-1), int)

while i < document_num:
	if documents[i][1] == 'pos':
		true_labels[i] = 1
	else:
		true_labels[i] = 0

	for w in documents[i][0]:
		if w.lower() in freq_dict:
			freq_dict[w.lower()]+=1

	print len(freq_dict)
	j = 0
	for key in sorted(freq_dict):
		corpus[i][j] = freq_dict[key]
		j+=1
		
	freq_dict = dict.fromkeys(vocabulary_words,0)
	i+=1

outfile = file('corpus.txt','w')
numpy.save(outfile, corpus)
outfile.close()
outfile = open('true_labels.txt', 'w')
numpy.save(outfile,true_labels)
outfile.close()

