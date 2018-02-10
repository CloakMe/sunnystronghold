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

dir_path = 'HTML_parsed01/'
n_samples = 20 #0 for all
n_features = 1000
n_components = 10
n_top_words = 20
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No command-line arguments, assume',dir_path,'for dir path of parsed htmls into jsons.')
    else:
        dir_path = sys.argv[1]
    
parsed_htmls = load_parsed_htmls.load_parsed_htmls(dir_path)
stringData = preprocess_docs.preprocess_docs(parsed_htmls)

lemmaToken = lemmatization.LemmaTokenizer()

tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                           max_features=n_features,
                                                                              stop_words='english', tokenizer = lemmaToken)

t0 = time()
tfidf = tfidf_vectorizer.fit_transform(stringData)
print("done in %0.3fs." % (time() - t0))
