from __future__ import unicode_literals

import gdata.youtube.service 
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import sys
import numpy
import pandas as pd
from collections import Counter

from matplotlib import pyplot
import matplotlib as mpl
import numpy as np
import mpld3


yts = gdata.youtube.service.YouTubeService() 
index = 1 

#data = fp.read().decode("utf-8-sig").encode("utf-8")
'''
todo: function load rating file. Also try to use panda.
'''
def read_sentiment_dictionary():
    data = pd.read_csv('journal.pone.0026752.s001.txt', sep='\t', usecols = [0, 2])\
                .set_index('word')['happiness_average'].to_dict()

    return {key: value for key, value in data.items() 
             if value < 3 or value > 7}
    
    
'''
todo: function load youtube comments.
'''
def retrieve_youtube_comments(videoId):
    urlpattern = 'http://gdata.youtube.com/feeds/api/videos/' + videoId + '/comments?start-index=%d&max-results=25' 
    url = urlpattern % index 
    comments = [] 
    while url: 
        try :
            
            ytfeed = yts.GetYouTubeVideoCommentFeed(uri=url) 
        except:
            break;
        #print (ytfeed)
        comments.extend([comment.content.text for comment in ytfeed.entry ])
        print("comments? " + str(len(comments)))  
        #print (ytfeed.GetNextLink())
        if (not hasattr(ytfeed.GetNextLink(), 'href')):
                    break;
        url = ytfeed.GetNextLink().href 
        #print url 
    return comments
    
    
'''
todo: function tokenize comments.
'''
def tokenize(comments):
    tokenComments = []
    for comment in comments:
        tokenizedComment = tokenizeComment(comment)
        if len (tokenizedComment) > 0:
            tokenComments.append(tokenizedComment)
#            tokenComments.append([word.lower().decode("utf-8-sig").encode("utf-8") for word in tokenizer.tokenize(comment)])
        
    return tokenComments    

def tokenizeComment(comment):
    out = []
    tokenizer = RegexpTokenizer(r'\w+')
    for word in tokenizer.tokenize(comment):
        try:
            out.append(word.lower().decode("utf-8-sig").encode("utf-8"))
        except:
            
            continue
    return out
    
    

'''
todo: function lemmatize comments.
'''
def lemmatize(tokens):
    tokenLemmas = [];
    lmtzr = WordNetLemmatizer()
    
    for items in tokens:
        tokenLemmas.append([lmtzr.lemmatize(item) for item in items])
    return tokenLemmas

def cleanStopWords(words):
    cleanWords = []
    for items in words:
        cleanWords.append([w for w in items if not w in stopwords.words('english')])
    return cleanWords
    
def calculateScore(commentsTokens, wordToRate):
    commentsSum = 0
    numOfComments = 0
    commentsToPlot=[]
    for comment in commentsTokens:
        
        if len(comment) == 0:
            continue
        commentMean = 0  
        count = 0
        for word in comment:
            atLeastOne = False
            
            if word in wordToRate:
                atLeastOne = True
                commentMean = commentMean + float(wordToRate[word])
                count = count + 1
        if atLeastOne:
            numOfComments = numOfComments + 1
            commentMean = commentMean / count
            commentsToPlot.append(commentMean)
            commentsSum = commentsSum + commentMean
    print commentsToPlot 
    heatmap(commentsToPlot,numOfComments,commentsSum / numOfComments)    
    return commentsSum / numOfComments



def heatmap(commentsToPlot,numOfComments,mean):
    x=commentsToPlot
    y=[]
    '''
    for i in commentsToPlot:
        y.append(Counter(i))
    '''
    N = numOfComments
    cmap = mpl.cm.cool
    norm = mpl.colors.Normalize(vmin=4, vmax=8)
    fig = pyplot.figure(figsize=(8,3))
    ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
    ax2 = fig.add_axes([0.05, 0.475, 0.9, 0.15])
    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                   norm=norm,
                                   orientation='horizontal')
    cb1.set_label('Some Units')

    bounds=[4,5,6,7,8]
    norm=mpl.colors.BoundaryNorm(bounds, cmap.N)
    cmap.set_over('0.25')
    cmap.set_under('0.75')

    # If a ListedColormap is used, the length of the bounds array must be
    # one greater than the length of the color list.  The bounds must be
    # monotonically increasing.

    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
                                         norm=norm,
                                         # to use 'extend', you must
                                         # specify two extra boundaries:
                                         boundaries=[0]+bounds+[13],
                                         extend='both',
                                         ticks=bounds, # optional
                                         spacing='proportional',
                                         orientation='horizontal')
    cb2.set_label('Discrete intervals, some other units')
    pyplot.show()
    
wordToRate = read_sentiment_dictionary()            
print(len(wordToRate))
comments = retrieve_youtube_comments("sRJOU0Fi9Ts")
tokenComments = tokenize(comments)
print(tokenComments)
tokenLemmas = lemmatize(tokenComments)
cleanComments = cleanStopWords(tokenLemmas) 
score = calculateScore(cleanComments, wordToRate)

print ("Score is : " + str(score))