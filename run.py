#!/usr/bin/env python
#use coherence to calculate how good are clusters - no training - only try to find best number of topics
#use proper stop words dictionary - add words to stop words, exclude words from stop words.
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

import cluster_on_word_combinations as prep_docs

dir_path = 'HTML_parsed01/'
n_samples = None #None for all
n_features = 99
n_components = 5
n_top_words = 10

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

def csv_to_string_data(csv_filepath, row_threshold):
    texts = []
    labels = []
    
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        row_count = sum(1 for row in reader)
        if row_threshold  is None:
            max_articles = row_count
        else:
            max_articles = row_threshold
        csvfile.seek(0)             # Reset file pointer to the beginning
        reader = csv.reader(csvfile)  # Create a new reader from the reset file object
        for row_num, row in enumerate(reader, start=1):
            # Skip empty rows or header if any (adapt if needed)
            if not row:
                continue
            if row_num >= max_articles:
                break
            # Example: Combine multiple columns as one document string
            # You can adjust which columns to combine for "document"
            # Here using columns 1 (title) and 3 (description) as text
            doc_text = row[3] + " " + row[1]
            texts.append(doc_text.strip())
            labels.append(row[6])  # Assuming label is in column 6
            
    return texts, labels

def get_gensim_coherence(sklearn_lda, tf_feature_names, texts, my_stop_words):
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
    tokenized_texts = [lemmaToken(doc) for doc in texts]
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

def get_rule_cluster_top_words(vectorcast_topics, tf_feature_names, texts, lemmaToken, my_stop_words):
    rule_topics = []
    for topic_idx, vc_topic in enumerate(vectorcast_topics):
        # Flatten word combinations into top words for this cluster
        flat_words = [word for combo in vc_topic for word in combo]
        # Optionally score/filter by TF-IDF relevance from your vectorizer
        relevant_words = [w for w in flat_words if w in tf_feature_names]
        rule_topics.append(relevant_words[:n_top_words])  # Limit to n_top_words
        print(f"Rule Cluster #{topic_idx}: {relevant_words[:n_top_words]}")
    return rule_topics

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No command-line arguments, assume',dir_path,'for dir path of parsed htmls into jsons.')
    else:
        dir_path = sys.argv[1]
    
    #parsed_htmls = load_parsed_htmls.load_parsed_htmls(dir_path, n_samples)
    #stringData = preprocess_docs.preprocess_docs(parsed_htmls)
    #pickle.dump( stringData, open('stringData.pickle','wb') )
    #stringData = pickle.load( open('stringData.pickle','rb') )
    all_texts, labels = csv_to_string_data('Issues_Vector21-periodicreview-oct25o.csv', n_samples)
    vectorcast_topics = [
        [ ['build', 'compil'], ['error', 'failure'] ],
        [ ['using source file perspective', 'source file perspective', 'sfp'], ['set', 'using'] ],
        [ ['link'], ['error', 'failure'] ],
        [ ['parse', 'environment'], ['error', 'failure'] ],
        [ ['license'], ['error'] ]
    ]
    simple_clusters = prep_docs.process_topics(vectorcast_topics, all_texts, n_samples)
    lemmaToken = lemmatization.LemmaTokenizer()
    
    vectorcastStopWords = {'previously', 'previous', 'vectorcast', 'fix', 'version', '2021', '2022', '2023', '2024', '2025', 'sp1', 'sp2', 'sp3', 'sp4', 'sp5', 'sp6', 'sp7'}
    vectorcastUseWords = {'no'}
    my_stop_words = list(text.ENGLISH_STOP_WORDS.union(vectorcastStopWords).difference(vectorcastUseWords))
    tfidf_vectorizer = TfidfVectorizer(max_df=0.7, 
                                       min_df=2,
                                       stop_words=my_stop_words, 
                                       tokenizer = lemmaToken,
                                       ngram_range=(2, 4))
    non_clustered_ids = [id for id,cluster in simple_clusters.items() if cluster == -1]
    texts = [all_texts[id] for id in non_clustered_ids]
    tfidf = tfidf_vectorizer.fit_transform(texts)


    print("Fitting LDA models with tf features, "
          "n_samples=%d and n_features=%d..."
          % (len(texts), n_features))

    lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
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
    
   
    print("coherence =", get_gensim_coherence(lda, tf_feature_names, texts, my_stop_words))
    
    vis_data = pyLDAvis.lda_model.prepare(lda, tfidf, tfidf_vectorizer)
        
    pyLDAvis.save_html(vis_data, 'lda_vis.html')
    #pyLDAvis.show(vis_data)
