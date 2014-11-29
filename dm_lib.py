"""
dm_lib module.

this module implements all the functions necessary
for loading sentiment dictionaries from files
and retrieving youtube data
"""

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import pandas as pd
from nltk.stem.lancaster import LancasterStemmer



#data = fp.read().decode("utf-8-sig").encode("utf-8")

def read_sentiment_dictionary():
    """Calculate the dictionary with words and their sentiment score."""
    data = pd.read_csv('journal.pone.0026752.s001.txt', sep='\t',\
            usecols=[0, 2]).set_index('word')['happiness_average'].to_dict()

    min_value = min(data.itervalues())
    max_value = max(data.itervalues())
    return {key: (5*(value - min_value)/(max_value - min_value))\
                for key, value in data.items() if value < 3 or value > 6}



def tokenize(comments):
    """
    Split all youtube video's comments into a lists of tokkens.
    
    Keyword arguments:
    comments -- The list of strings to tokenize
    """
    token_comments = []
    for comment in comments:
        tokenized_comment = tokenize_comment(comment)
        if len(tokenized_comment) > 0:
            token_comments.append(tokenized_comment)
    return token_comments

def tokenize_comment(comment):
    """
    Split comment into words/tokkens.
    
    Keyword arguments:
    comment -- The comment to tokenize
    """
    out = []
    tokenizer = RegexpTokenizer(r'\w+')
    try:
        for word in tokenizer.tokenize(comment):
            try:
                out.append(word.lower().decode("utf-8-sig").encode("utf-8"))
            except:
                continue
        return out
    except:
        return []


def lemmatize(tokens):
    """
    Lematize a list of tokens.
    
    Keyword arguments:
    tokens -- The list of tokens to lemmatize
    """
    token_lemmas = []
    stemmer = LancasterStemmer()

    for items in tokens:
        try:
            token_lemmas.append([stemmer.stem(item) for item in items])
        except:
            continue
    return token_lemmas

def clean_stop_words(words):
    """
    Clean all stop words from a list of lists of words.

    Keyword arguments:
    words -- a list of lists of words
    """
    clean_words = []
    for items in words:
        clean_words.append(\
                    [w for w in items if not w in stopwords.words('english')])
    return clean_words

def calculate_score(comments_tokens, word_to_rate):
    """
    Calculate the sentiment score for a video.
    
    Keyword arguments:
    comments_tokens -- the tokens from the comments for a video
    word_to_rate -- the dictionary with the word's rating
    """
    comments_sum = 0
    num_of_comments = 0
    individual_scores = []
    for comment in comments_tokens:

        if len(comment) == 0:
            continue
        comment_mean = 0
        count = 0
        for word in comment:
            at_least_one = False

            if word in word_to_rate:
                at_least_one = True
                comment_mean = comment_mean + float(word_to_rate[word])
                count = count + 1
        if at_least_one:
            num_of_comments = num_of_comments + 1
            comment_mean = comment_mean / count
            comments_sum = comments_sum + comment_mean
            individual_scores.append(comment_mean)

    return (comments_sum / num_of_comments, individual_scores)


if __name__ == "__main__":
    get_channel_videos("smosh")
