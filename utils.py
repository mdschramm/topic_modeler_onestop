import matplotlib.pyplot as plt
import json
import hashlib
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import nltk
from nltk.stem import PorterStemmer
import re
import os
import csv

# filters for words
pattern = re.compile('[\W_]+')
stop_words = set(stopwords.words('english'))

nltk.download('punkt')

# Initialize the Porter Stemmer
porter_stemmer = PorterStemmer()

def sort_data_by_date(filename, datecol):
    data = pd.read_csv(filename)
    print(data)

    data[datecol]
    # Convert the string column to datetime
    data[datecol] = pd.to_datetime(data[datecol])

    # Sort the DataFrame by the datetime column in ascending order
    df_sorted = data.sort_values(by=datecol)

    return df_sorted



def process_description(body):
    soup = BeautifulSoup(body, 'html.parser')
    text = soup.get_text().lower()
    text = pattern.sub(' ', text)
    tokens = word_tokenize(text)
    filtered_words = set(tokens) - set(stop_words)
    
    return text, filtered_words

MUSE_LISTINGS = 'muse/LISTINGS_FILE.csv'
ONESTOP_LISTINGS = 'onestop/LISTINGS_FILE.csv'

def order_csv_by_date(filename):
    df = pd.read_csv(filename, parse_dates=['date_posted'])
    df = df.sort_values('date_posted')
    df.to_csv(filename)

# order_csv_by_date(MUSE_LISTINGS)
# order_csv_by_date(ONESTOP_LISTINGS)

def is_duplicate(hashes, job_description):
    hash = hashlib.md5(job_description.encode('utf-8')).hexdigest()
    if hash in hashes:
        return True
    hashes.add(hash)
    return False

# Octis stuff
# Takes a downloaded LISTINGS_FILE.csv and outputs a directory to be used by OCTIS:
# https://github.com/MIND-Lab/OCTIS?tab=readme-ov-file#load-a-custom-dataset 

OCTIS_DATA_PATH = 'octis_data'
DESCRIPTION = 'description'

def create_octis_dataset(source_filepath):
    # 2 columns - description, train (train or val)
    corpus_filename = 'corpus.txt'
    # newline separate list of all words in the corpus
    vocabulary_filename = 'vocabulary.txt'
    vocab = set()
    # create parent dir
    dirname = os.path.join(OCTIS_DATA_PATH, os.path.dirname(source_filepath))
    os.makedirs(dirname, exist_ok=True)
    
    # De-duplicate
    hashes = set()

    with open(source_filepath, 'r') as sf, \
        open(os.path.join(dirname, corpus_filename), 'w') as corpus:
        source_reader = csv.DictReader(sf)

        for line in source_reader:
            job_description = line[DESCRIPTION]
            text, filtered_words = process_description(job_description)
            if is_duplicate(hashes, text):
                continue
            corpus.write(text + '\n')
            vocab |= filtered_words
    with open(os.path.join(dirname, vocabulary_filename), 'w') as vf:
        for word in vocab:
            vf.write(word + '\n')


# create_octis_dataset(MUSE_LISTINGS)
# create_octis_dataset(ONESTOP_LISTINGS)


SOURCE_FILE = 'optimize_result/lda_onestop/result.json'
def graph_lda_optimization(source_file):
    result = json.load(open(source_file, 'r'))
    x_vals = result['x_iters']['num_topics']
    y_vals = result['f_val']
    plt.scatter(x_vals, y_vals)
    plt.title('Coherence score vs. num_topics')
    plt.xlabel('num_topics')
    plt.ylabel('Coherence score')
    plt.show()

# graph_lda_optimization(SOURCE_FILE)