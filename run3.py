#!/usr/bin/env python
#use guidedlda for supervised clustering
from __future__ import print_function
import csv
import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
import guidedlda
import pyLDAvis
import pyLDAvis.lda_model
import lemmatization

n_samples = 100 #None for all

def prepare_guidedlda_pyldavis(model, X_counts, vocab):
    # topic-term distributions, shape (n_topics, n_vocab)
    topic_term_dists = model.topic_word_

    # document-topic distributions, shape (n_docs, n_topics)
    doc_topic_dists = model.transform(X_counts)

    # calculate document lengths (number of words per doc)
    doc_lengths = np.array(X_counts.sum(axis=1)).flatten()

    # calculate term frequency over the corpus (sum across docs)
    term_frequency = np.array(X_counts.sum(axis=0)).flatten()

    # create a dictionary with pyLDAvis expected format
    prepared_data = pyLDAvis.prepare(
        topic_term_dists=topic_term_dists,
        doc_topic_dists=doc_topic_dists,
        doc_lengths=doc_lengths,
        vocab=vocab,
        term_frequency=term_frequency
    )
    return prepared_data


def csv_to_string_data_and_labels(csv_filepath):
    texts = []
    labels = []
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row_num, row in enumerate(reader, start=1):
            if not row:
                continue
            if row_num > n_samples:
                break
            # Use columns 1 and 3 as text; adjust if needed
            doc_text = row[1] + " " + row[3]
            texts.append(doc_text.strip())
            labels.append(row[6])  # Assuming label is in column 6
    return texts, labels

# Function to check if document contains any seed word tokens
def contains_seed_words(doc_idx, seed_word_ids):
    doc_tokens = X_counts[doc_idx].indices
    return any(token in doc_tokens for token in seed_word_ids)

if __name__ == "__main__":
    csv_filepath = 'Issues_Vector21-periodicreview-oct25o.csv'
    if len(sys.argv) > 1:
        csv_filepath = sys.argv[1]

    print(f"Loading data from {csv_filepath}...")
    texts, labels = csv_to_string_data_and_labels(csv_filepath)

    print("Vectorizing text with CountVectorizer for guidedLDA...")
    vectorcastStopWords = {'previously', 'previous', 'vectorcast', 'fix', 'version', '2021', '2022', '2023', '2024', '2025'}
    vectorcastUseWords = {'no'}
    my_stop_words = list(text.ENGLISH_STOP_WORDS.union(vectorcastStopWords).difference(vectorcastUseWords))
    lemmaToken = lemmatization.LemmaTokenizer()
    count_vectorizer = CountVectorizer(stop_words=my_stop_words, 
                                       min_df=1,
                                       max_df=0.7,
                                       tokenizer = lemmaToken,
                                       ngram_range=(1, 3))
    X_counts = count_vectorizer.fit_transform(texts)
    vocab = count_vectorizer.get_feature_names_out()

    # Define your seed words for supervised topics (clusters)
    seed_topics = {
        0: ['build', 'compiler', 'compilation', 'compile'],
        1: ['source', 'file', 'perspective', 'sfp', 'report'],
        2: ['link', 'linker', 'linking'],
        3: ['parse'],
        4: ['environment']
    }

    # Map seed words to vocabulary indices for guidedLDA
    # seed_topics_indices should be dictionary {word_id: topic_id}
    seed_topics_indices = {}
    for topic_id, seed_words in seed_topics.items():
        for word in seed_words:
            if word in vocab:
                seed_topics_indices[vocab.tolist().index(word)] = topic_id
    
    
    n_topics = len(seed_topics)
    print("Fitting guidedLDA model with seed topics...")
    model = guidedlda.GuidedLDA(n_topics=n_topics, n_iter=100, random_state=7, refresh=20)
    model.fit(X_counts, seed_topics=seed_topics_indices, seed_confidence=0.15)
    
    print("Transforming documents into topic distributions...")
    doc_topic_dist = model.transform(X_counts)

    # doc_topic_dist: matrix of shape (n_docs, n_topics) from guidedlda.transform()
    assigned_clusters = doc_topic_dist.argmax(axis=1)
    max_probabilities = doc_topic_dist.max(axis=1)
    
    # Define cluster -1 as trash cluster
    trash_cluster_id = -1
    # Define threshold for confident cluster assignment; e.g., 0.3 (tune as needed)
    threshold = 0.9
    
    # Prepare flat list of all seed word IDs from your seed_topics dictionary
    seed_word_ids = [word_id for word_id in seed_topics_indices.keys()]
    
    final_clusters = []
    for idx in range(doc_topic_dist.shape[0]):
        if max_probabilities[idx] < threshold or not contains_seed_words(idx, seed_word_ids):
            final_clusters.append(trash_cluster_id)  # Assign to trash cluster
        else:
            final_clusters.append(assigned_clusters[idx])
    
    for special_id in range(-1,5):
        for idx, cluster in enumerate(final_clusters):
            if cluster == special_id:
                print(f"Document {idx}: Cluster {cluster} - Text Sample: {texts[idx][:100]}")
    
    # Optionally evaluate clustering against known labels if meaningful
    # For demonstration, just print some cluster examples
    
    # Use the function to prepare the visualization data
    vis_data = prepare_guidedlda_pyldavis(model, X_counts, vocab)
        
    pyLDAvis.save_html(vis_data, 'guidedlda_vis.html')

