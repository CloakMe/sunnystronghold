"""
Datathon critical outliers - clusterize VMWare KB articles

Credit to 
# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck
#         Chyi-Kwei Yau <chyikwei.yau@gmail.com>
for some source code from
http://scikit-learn.org/0.18/auto_examples/applications/topics_extraction_with_nmf_lda.html
"""

from __future__ import print_function
from time import time
import parse

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups

n_samples = 20 #0 for all
n_features = 1000
n_components = 10
n_top_words = 20

parsedHtmls = parse.ParseHtmlFiles(max_num_files=n_samples)
