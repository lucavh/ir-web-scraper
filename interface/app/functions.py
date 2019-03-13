from __future__ imports
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