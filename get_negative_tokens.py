# run separately beforehand

# import nltk
# nltk.download('punkt')

# pip install nltk transformers vaderSentiment
# _____________________________________________________________

import nltk
from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import string
import re

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
    with open(input_file, 'r') as file:
        lines = file.readlines()
        
    all_negative_phrases = []
    for line in lines:
        sentences = tokenize_text(line)
        negative_phrases = get_negative_phrases(sentences)
        all_negative_phrases.extend(negative_phrases)
        
    write_negative_phrases_to_file(all_negative_phrases, output_file)

detect_negative_phrases('/content/chatgpt-reddit-comments.csv', 'negative_tokens.txt')
