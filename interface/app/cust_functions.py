from collections import Counter,defaultdict
from bs4 import BeautifulSoup
import os
import glob
import nltk
import math
import re
import string
import pickle
import csv

def process_input(query):
    return [w for w in [w.strip(string.punctuation) for w in nltk.word_tokenize(query.lower())] if w != '']

def rankedSearchTFIDF(query,index):
    """
    Given a query, score the documents according to the tf-idf scoring
    scheme and print the documents and scores in decreasing order.
    """

    invertedIndex = pickle.load( open( index, "rb" ) )
    processed_input = process_input(query)

    scores = defaultdict(float)
    for t in processed_input:
        for d in invertedIndex[t]:
            scores[d] += invertedIndex[t][d]

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]