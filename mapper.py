#!/usr/bin/python3
"""

This mapper cleans and outputs the data related to each comment. Its output is in the following format:
a-subredditname-c-1
a-subredditname-t-topic
b-username-c-1 
b-username-t-topic 
c-commentID a controversiality
c-commentParentID b 1
d-topic upvotes downvotes positivity negativity 

"""

import json 
import sys
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.util import bigrams
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
nltk.download('wordnet')

# Define list of stop words and remove apostrophes
stopwords = ['i', 'im', 'ive', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'pretty', 'sure', 'also', 'your', 'yep', 'yes', 'no', 'nah', 'theyre', 'were', 'yours', 'yourself', 'yourselves', 'hes', 'shes', 'also', 'still', 'really', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
            'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 
            'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
            'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", "would", 'wouldn', "wouldn't", "like", "very", "good", "could", "couldn't", "please", "automatically"]
stopwords = [word.replace("'", "") for word in stopwords]

# This function checks if a character is English or not
def isEnglish(letter):
    if ord(letter) < 97 or ord(letter) > 122:
        return False
    else:
        return True

# This function cleans a string and returns it as a list of English lowercase words
def clean(line):

    # Remove numbers and all punctuation but retain forward slashes (to be removed later in with links)
    alpha_only = "".join(t.lower() for t in line if t.isalpha() or t == ' ' or t == '/')

    # Remove all stop words and words with forward slashes (links) unless they are a part of a subreddit name
    no_stops = [t for t in alpha_only.strip().split() if t not in stopwords and ('/' not in t or ' r/' in t)]

    # Instantiate the WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()

    # Lemmatize all tokens into a new list
    lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]   

    # Remove non-English words
    english_only = [w for w in lemmatized if isEnglish(w[0])]

    # Extract Bigrams, sort each pair and remove duplicates
    bgrams = bigrams(english_only)
    bgrams = list(set([tuple(sorted(element)) for element in bgrams]))

    return bgrams

# Create a SentimentIntensityAnalyzer object.
sid_obj = SentimentIntensityAnalyzer()

for line in sys.stdin:

    # Load JSON object from String
    comment = json.loads(line)

    # Extract comment attributes
    body = comment['body']
    subname = comment['subreddit']
    author = comment['author']
    commentid = comment['name']
    parentid = comment['parent_id']
    controversiality = comment['controversiality']
    ups = comment['ups']
    downs = comment['downs']

    # If any of the important fields are empty, ignore the comment
    if subname == '' or body == '' or author == '' or commentid == '' or parentid == '' or controversiality == '' or ups == '' or downs == '':
        continue

    # Clean comment body 
    body_cleaned = clean(body)
    
    # If the comment body is empty after being cleaned, ignore it
    if len(body_cleaned) == 0:
        continue
    
    # If the author is deleted, ignore their comment
    if author == "[deleted]":
        continue

    # Replace each - in the author's name with a # because we use dashes in our keys
    author = author.replace("-", "#")

    # Extract the number of upvotes and downvotes. If any of them is negative, ignore the comment
    ups = int(ups)
    downs = int(downs)
    if ups<0 or downs<0:
        continue

    # Find comment sentiment value
    sentiment_dict = sid_obj.polarity_scores(body)
    pos = round(sentiment_dict['pos']*100)
    neg = round(sentiment_dict['neg']*100)

    # Print comment data
    print('a',subname,'c', '1', sep='-')
    print('b',author,'c', '1', sep='-')
    
    for item in body_cleaned: 
        print('a', subname, 't', item, sep='-')
        print('b', author, 't', item, sep='-')
        print('d-', item, '\t', ups, '\t', downs, '\t', pos, '\t', neg, sep='')
        
    print('c-', commentid, '\ta\t', controversiality, sep='')

    # Print the parent ID only if the parent is a comment (Its ID starts with 't1')
    if parentid[0] == 't' and parentid[1] == '1':
        print('c-', parentid, '\tb\t', '1', sep='')

        

