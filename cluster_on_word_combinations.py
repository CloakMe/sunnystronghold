#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 16:15:31 2025
using predefined word combinations to create some initial clusters
e.g. (compil OR build) AND (error OR failure)
"""

import csv
import sys

""" combination = [[compil, build], [error, fail]]"""
def find_word_combination(combination, bug_description):
    for item in combination:
        sub_item_found = False;
        for sub_item in item:
            sub_item_found = bug_description.lower().find(sub_item) != -1
            if sub_item_found == True:
                break
        if sub_item_found == False:
            return False
    return True

#n_samples = 620 #None for all

#csv_filepath = 'Issues_Vector21-periodicreview-oct25o.csv'

def process_topics(vectorcast_topics, texts, n_samples):
    
    if len(sys.argv) > 1:
        csv_filepath = sys.argv[1]

    simple_clusters = {}
    t_i = 0
    for bug_description in texts:
        idx = 0
        for vc_topic in vectorcast_topics:        
            res = find_word_combination(vc_topic, bug_description)
            if(res == True):
                simple_clusters[t_i]=idx
                break
            else:
                simple_clusters[t_i]=-1
            idx = idx+1
        if(t_i == 15):
            breakHere = 1
        t_i = t_i + 1
        
    size = len(vectorcast_topics)
    print('size = ', len(simple_clusters))
    for special_id in range(-1, size):
        count = 0
        for doc_idx, cluster_id in simple_clusters.items():  # Proper iteration
            if cluster_id == special_id:
                print(f"Document {doc_idx}: Cluster {cluster_id} - Text Sample: {texts[doc_idx][:100]}")
                count += 1
        if count == 0:
            print(f"No documents in cluster {special_id}")
    
    return simple_clusters
                
    