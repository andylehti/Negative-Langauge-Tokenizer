# run separately beforehand

# import nltk
# nltk.download('punkt')

# pip install nltk transformers vaderSentiment pandas collections
# _____________________________________________________________

import nltk
from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import string
import re
import pandas as pd
from collections import Counter
import json
import xml.etree.ElementTree as ET
import csv
from sqlalchemy import create_engine
import sqlite3

def extract_usable_data(input_file):
    extension = input_file.split('.')[-1]
    unique_lines = []

    if extension == 'xlsx':
        data = pd.read_excel(input_file)
        for i in data.columns:
            for item in data[i]:
                unique_lines.append(str(item))

    elif extension == 'csv':
        with open(input_file, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                unique_lines.extend(row)

    elif extension == 'json':
        with open(input_file) as f:
            data = json.load(f)
            for item in data:
                unique_lines.append(str(item))

    elif extension == 'xml':
        tree = ET.parse(input_file)
        root = tree.getroot()
        for elem in root.iter():
            unique_lines.append(elem.text)

    elif extension == 'sql':
        database = create_engine('sqlite:///' + input_file)
        query = "SELECT * FROM tablename" # Replace with your table name
        data = pd.read_sql_query(query, database)
        for i in data.columns:
            for item in data[i]:
                unique_lines.append(str(item))

    return unique_lines

def tokenize_text(input_text):
    # remove punctuation and lowercase the text
    input_text = re.sub(r'[^\w\s]', '', input_text).lower()
    sentences = sent_tokenize(input_text)
    return [nltk.word_tokenize(sent) for sent in sentences]

def get_negative_phrases(sentences):
    analyzer = SentimentIntensityAnalyzer()
    negative_phrases = []
    
    # check if the 2-3 word phrases are negative
    for sentence in sentences:
        for i in range(len(sentence)-2):
            three_word_phrase = ' '.join(sentence[i:i+3])
            two_word_phrase = ' '.join(sentence[i:i+2])

            if analyzer.polarity_scores(three_word_phrase)['compound'] < 0:
                negative_phrases.append(three_word_phrase)

            elif analyzer.polarity_scores(two_word_phrase)['compound'] < 0:
                negative_phrases.append(two_word_phrase)

    return negative_phrases

def write_negative_phrases_to_file(negative_phrases, filename='negative_phrases.txt'):
    with open(filename, 'w') as file:
        for phrase in negative_phrases:
            file.write(phrase + '\n')

def detect_negative_phrases(input_file, output_file):
    data = extract_usable_data(input_file)

    all_negative_phrases = []
    for line in data:
        # Remove lines with words longer than 18 characters
        if not any(len(word) > 18 for word in line.split()):
            sentences = tokenize_text(line)
            negative_phrases = get_negative_phrases(sentences)
            all_negative_phrases.extend(negative_phrases)

    write_negative_phrases_to_file(all_negative_phrases, output_file)

detect_negative_phrases('/content/chatgpt-reddit-comments.csv', 'output.txt')
