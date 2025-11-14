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

from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups
import numpy as np

import pyLDAvis
import pyLDAvis.lda_model
#import cPickle as pickle
import csv

import nltk
nltk.data.path.append('/home/admin/nltk_data')

from gensim.test.utils import common_corpus, common_dictionary
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora.dictionary import Dictionary

dir_path = 'HTML_parsed01/'
n_samples = 100 #None for all
n_features = 100
#n_components = 4
n_top_words = 7

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

def csv_to_string_data(csv_filepath):
    string_data = {"text": []}

    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row_num, row in enumerate(reader, start=1):
            # Skip empty rows or header if any (adapt if needed)
            if not row:
                continue
            if row_num > n_samples:
                break
            # Example: Combine multiple columns as one document string
            # You can adjust which columns to combine for "document"
            # Here using columns 1 (title) and 3 (description) as text
            doc_text = row[1] + " " + row[3]
            string_data["text"].append(doc_text.strip())
    
    return string_data

def get_gensim_coherence(sklearn_lda, tf_feature_names, stringData, my_stop_words):
    # tokenized_texts: list of documents, each document is a list of tokens (words)
    topics = []
    for topic_idx, topic_weights in enumerate(sklearn_lda.components_):
        top_word_indices = topic_weights.argsort()[:-n_top_words-1:-1]
        top_words = [tf_feature_names[i] for i in top_word_indices]
        topics.append(top_words)
    
    #topics_tokenized = [[phrase.split() for phrase in topic] for topic in topics]
    topics_tokenized = [
        [token for phrase in topic for token in phrase.split()]
        for topic in topics
    ]
    tokenized_texts = [lemmaToken(doc) for doc in stringData["text"]]
    dictionary = Dictionary(tokenized_texts)
    bug_common_corpus = [
        dictionary.doc2bow([token for token in doc_tokens if token not in my_stop_words])
        for doc_tokens in tokenized_texts
    ]
    
    #print(type(common_corpus))  # should be list or gensim iterable
    #print(type(common_corpus[0]))  # should be list of tuples
    #print(common_corpus[0])  # e.g. [(0, 2), (5, 3)] first doc’s bow representation
    #for topic in topics:
    #    for word in topic:
    #        print(word, type(word))
 
    cm = CoherenceModel(topics=topics_tokenized, corpus=bug_common_corpus, dictionary = dictionary, coherence='u_mass')
        
    coherence = cm.get_coherence()  # get coherence value

    return coherence
    
def generate_sklearn_topics_coherence(my_stop_words, lemmaToken, stringData, num_topics):
    tfidf_vectorizer = TfidfVectorizer(max_df=0.90, 
                                       min_df=2,
                                       max_features=n_features, 
                                       stop_words=my_stop_words, 
                                       tokenizer = lemmaToken,
                                       ngram_range=(2, 3))


    tfidf = tfidf_vectorizer.fit_transform(stringData["text"])



    print("Fitting LDA models with tf features, "
          "n_samples=%d and n_features=%d..."
          % (n_samples, n_features))

    lda = LatentDirichletAllocation(n_components=num_topics, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    t0 = time()
    lda.fit(tfidf)
    print("done in %0.3fs." % (time() - t0))

    print("\nTopics in LDA model:")
    tf_feature_names = tfidf_vectorizer.get_feature_names_out()
    topwords = print_top_words(lda, tf_feature_names, n_top_words)
    print("done in %0.3fs." % (time() - t0))
    
    coherence = get_gensim_coherence(lda, tf_feature_names, stringData, my_stop_words)
    print("coherence =", coherence)
    return lda, coherence

    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No command-line arguments, assume',dir_path,'for dir path of parsed htmls into jsons.')
    else:
        dir_path = sys.argv[1]
    
    #parsed_htmls = load_parsed_htmls.load_parsed_htmls(dir_path, n_samples)
    #stringData = preprocess_docs.preprocess_docs(parsed_htmls)
    #pickle.dump( stringData, open('stringData.pickle','wb') )
    #stringData = pickle.load( open('stringData.pickle','rb') )
    stringData = csv_to_string_data('Issues_Vector21-periodicreview-oct25o.csv')
    lemmaToken = lemmatization.LemmaTokenizer()
    
    vectorcastStopWords = {'problem', 'previously', 'previous', 'vectorcast', 'fix', 'version', '2021', '2022', '2023', '2024', '2025', 'sp1', 'sp2', 'sp3', 'sp4', 'sp5', 'sp6', 'sp7', 'sp8'}
    vectorcastUseWords = {'no'}
    my_stop_words = list(text.ENGLISH_STOP_WORDS.union(vectorcastStopWords).difference(vectorcastUseWords))
    
    start = 2
    stop = 10
    model_list = []
    coh_list = []
    
    for num_topics in range(start, stop, 1):
        lda, coherence = generate_sklearn_topics_coherence(my_stop_words, lemmaToken, stringData, num_topics)
        model_list.append(lda)
        coh_list.append(coherence)
        
    import matplotlib.pyplot as plt
    x = range(start, stop, 1)
    plt.plot(x, coh_list)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence Score")
    plt.show()
    
    # Choose the number of topics with highest coherence
    optimal_num_topics = x[coh_list.index(max(coh_list))]
    print("Optimal number of topics:", optimal_num_topics)

    #pyLDAvis.show(vis_data)
