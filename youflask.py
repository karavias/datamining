from flask import Flask


app = Flask(__name__)

@app.route("/")
def hello():
    wordToRate = read_sentiment_dictionary()            
    print(len(wordToRate))
    comments = retrieve_youtube_comments("sRJOU0Fi9Ts")
    tokenComments = tokenize(comments)
    print(tokenComments)
    tokenLemmas = lemmatize(tokenComments)
    cleanComments = cleanStopWords(tokenLemmas) 
    score = calculateScore(cleanComments, wordToRate)
    
    print ("Score is : " + str(score))
    return "Hello World!"
    
    
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
    

if __name__ == "__main__":
    app.run()