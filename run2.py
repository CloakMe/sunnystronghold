#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import sys
import csv
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

import lemmatization

def csv_to_string_data_and_labels(csv_filepath):
    texts = []
    labels = []
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:
                continue
            # Example: Use columns 1 and 3 as text; column 0 as label - adjust as needed
            doc_text = row[1] + " " + row[3]
            texts.append(doc_text.strip())
            labels.append(row[6])  # Assuming label is in column 0
    return texts, labels

if __name__ == "__main__":
    csv_filepath = 'Issues_Vector21-periodicreview-oct25o.csv'
    if len(sys.argv) > 1:
        csv_filepath = sys.argv[1]

    print(f"Loading data from {csv_filepath}...")
    texts, labels = csv_to_string_data_and_labels(csv_filepath)

    print("Preprocessing and vectorizing text...")
    lemmaToken = lemmatization.LemmaTokenizer()
    tfidf_vectorizer = TfidfVectorizer(
                            max_df=0.95,
                            min_df=2,
                            max_features=100,
                            stop_words='english',
                            tokenizer=lemmaToken)
    X = tfidf_vectorizer.fit_transform(texts)
    y = labels

	#in sklearn splits your dataset into four parts, each with a specific role:
    #X: The input feature matrix (all samples with their features).
    #y: The target labels corresponding to each sample in X.
    #
#The outputs are:

    #X_train: The subset of X used to train the model (here 80% of data).
    #X_test: The subset of X reserved for testing or evaluating the model (here 20% of data).
    #
    #y_train: The labels corresponding to X_train.
    #y_test: The labels corresponding to X_test.
	#
#Parameters:
    #test_size=0.2: 20% of the dataset will be randomly selected as the test set, and 80% as the training set.
    #random_state=42: A fixed seed for the random number generator to ensure reproducible splits every time you run the code.
	#In summary, this function randomly shuffles and splits 
	#the input data and labels into training and testing sets according to the specified test size, 
	#maintaining the input-label correspondence for supervised learning. The training sets are used 
	#to fit the model, while the test sets evaluate its performance in an unbiased manne
	
    print("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
                                            X, y, test_size=0.2, random_state=42)

    print("Training Logistic Regression model...")
    clf = LogisticRegression(max_iter=200)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print(f"Training done in {train_time:.3f}s.")

    print("Predicting on test set...")
    y_pred = clf.predict(X_test)

    print("Evaluation results:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Optionally, save the model or vectorizer for later use
    # via pickle or joblib if needed
    
    # Convert y_test to a numpy array if not already
y_test_array = np.array(y_test)

# Find indices where predictions differ from true labels
misclassified_indices = np.where(y_test_array != y_pred)[0]

print("Misclassified entries:")
for idx in misclassified_indices:
    print(f"Index: {idx}")
    print(f"True label: {y_test_array[idx]}")
    print(f"Predicted label: {y_pred[idx]}")
    # To show the original text corresponding to this index in test set
    # you need to map back from X_test to original texts:
    # Assuming you kept texts in the same order and did not shuffle outside train_test_split:
    print(f"Text: {texts[idx]}")  
    print("-----")

