#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 16:15:31 2025
using predefined word combinations to create some initial clusters
e.g. (compil OR build) AND (error OR failure)
"""

""" combination = [[compil, build], [error, fail]]"""
def find_word_combination(combination, bug_description):
    for item in combination:
        sub_item_found = False;
        for sub_item in item:
            sub_item_found = bug_description.find(sub_item) != -1
            if sub_item_found == True:
                break
        if sub_item_found == False:
            return False
    return True

if __name__ == "__main__":
    csv_filepath = 'Issues_Vector21-periodicreview-oct25o.csv'
    if len(sys.argv) > 1:
        csv_filepath = sys.argv[1]

    print(f"Loading data from {csv_filepath}...")
    texts, labels = csv_to_string_data_and_labels(csv_filepath)
    
    vectorcast_topics = [
        [ ['build', 'compil'], ['error', 'failure'] ],
        [ ['source file perspective', 'sfp'], ['report'] ],
        [ ['link'], ['error', 'failure'] ],
        [ ['parse', 'environment'], ['error', 'failure'] ]
    ]
    for list_item in vectorcast_topics:
        for text in texts:
            find_word_combination(combination, bug_description):
    