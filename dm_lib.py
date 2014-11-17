import gdata.youtube.service 
from nltk import word_tokenize
#from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import sys
import numpy
import pandas as pd
from nltk.stem.lancaster import LancasterStemmer
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
    yts = gdata.youtube.service.YouTubeService() 
    index = 1 
    urlpattern = 'http://gdata.youtube.com/feeds/api/videos/' + videoId + '/comments?start-index=%d&max-results=25' 
    url = urlpattern % index 
    comments = [] 
    while url: 
        try :
            
            ytfeed = yts.GetYouTubeVideoCommentFeed(uri=url) 
            
        except:
            break;
        #print (ytfeed)
        for comment in ytfeed.entry:
            print(comment.published.text)
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
    st = LancasterStemmer()
    #lmtzr = WordNetLemmatizer()
    
    for items in tokens:
        tokenLemmas.append([st.stem(item) for item in items])
    return tokenLemmas

def cleanStopWords(words):
    cleanWords = []
    for items in words:
        cleanWords.append([w for w in items if not w in stopwords.words('english')])
    return cleanWords
    
def calculateScore(commentsTokens, wordToRate):
    commentsSum = 0
    numOfComments = 0
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
            commentsSum = commentsSum + commentMean
        
    return commentsSum / numOfComments
    
    
def get_top_videos():
    '''
    Get top videos
    '''
    yt_service = gdata.youtube.service.YouTubeService()
    feed = yt_service.GetMostViewedVideoFeed()
    return feed

def get_top_videos_comments():
    feed = get_top_videos()
    out = {}
    for video in feed.entry:
        videoId = video.media.player.url.split('v=')[1].split('&')[0]
        print("#####comments for " + videoId + "######")
        print(retrieve_youtube_comments(videoId))
        
        #print_entry_details(video)
#        print(str(video.media.title.text) + " = " + str(video.rating.average))

def print_video_feed(feed):
    for entry in feed.entry:
        print_entry_details(entry)
        


def print_entry_details(entry):
    print 'Video title: %s' % entry.media.title.text
    print 'Video published on: %s ' % entry.published.text
    print 'Video description: %s' % entry.media.description.text
    #print 'Video category: %s' % entry.media.category[[]0].text
    print 'Video tags: %s' % entry.media.keywords.text
    print 'Video watch page: %s' % entry.media.player.url
    print 'Video flash player URL: %s' % entry.GetSwfUrl()
    print 'Video duration: %s' % entry.media.duration.seconds

      # non entry.media attributes
#    print 'Video geo location: %s' % entry.geo.location()
    print 'Video view count: %s' % entry.statistics.view_count
    print 'Video rating: %s' % entry.rating.average

    # show alternate formats
    for alternate_format in entry.media.content:
        if 'isDefault' not in alternate_format.extension_attributes:
            print 'Alternate format: %s | url: %s ' % (alternate_format.type, alternate_format.url)

    # show thumbnails
    for thumbnail in entry.media.thumbnail:
        print 'Thumbnail url: %s' % thumbnail.url

if __name__ == "__main__":
    get_top_videos_comments()
'''    
    wordToRate = read_sentiment_dictionary()            
    print(len(wordToRate))
    comments = retrieve_youtube_comments("sRJOU0Fi9Ts")
    tokenComments = tokenize(comments)
    print(tokenComments)
    tokenLemmas = lemmatize(tokenComments)
    cleanComments = cleanStopWords(tokenLemmas) 
    score = calculateScore(cleanComments, wordToRate)
    print(score)
   ''' 