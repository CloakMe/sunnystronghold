#!/usr/bin/env python
#Datathon critical outliers - clusterize VMWare KB articles

#Credit to 
# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck
#         Chyi-Kwei Yau <chyikwei.yau@gmail.com>
#for some source code from
#http://scikit-learn.org/0.18/auto_examples/applications/topics_extraction_with_nmf_lda.html

from __future__ import print_function
import os
import sys
from time import time
#import parse
import load_parsed_htmls
import preprocess_docs
import lemmatization

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups
import numpy as np

dir_path = 'HTML_parsed01/'
n_samples = 20 #None for all
n_features = 1000
n_components = 10
n_top_words = 20
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No command-line arguments, assume',dir_path,'for dir path of parsed htmls into jsons.')
    else:
        dir_path = sys.argv[1]
    
parsed_htmls = load_parsed_htmls.load_parsed_htmls(dir_path, n_samples)
stringData = preprocess_docs.preprocess_docs(parsed_htmls)

lemmaToken = lemmatization.LemmaTokenizer()
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,max_features=n_features, stop_words='english', tokenizer = lemmaToken)
tfidf = tfidf_vectorizer.fit_transform(stringData["text"])
def print_top_words(model, feature_names, n_top_words):
    outstr = []
    for topic_idx, topic in enumerate(model.components_):
        ascendingIndeces = topic.argsort()[:-n_top_words - 1:-1]
        message = "Topic #%d: " % topic_idx
        sublist = []
        for idx in ascendingIndeces:
            message += (feature_names[idx] + '\n')
            sublist += [feature_names[idx]]
        outstr += [sublist]
        print(message)
    print()
    return outstr

print("Fitting LDA models with tf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
lda = LatentDirichletAllocation(n_topics=n_components, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
t0 = time()
lda.fit(tfidf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in LDA model:")
tf_feature_names = tfidf_vectorizer.get_feature_names()
topwords = print_top_words(lda, tf_feature_names, n_top_words)
print("done in %0.3fs." % (time() - t0))
