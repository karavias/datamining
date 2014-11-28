from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import dm_lib as dm
import time
import iovideocache as ioc
import dm_matLib as dmMat

app = Flask(__name__)
wordToRate = dm.read_sentiment_dictionary()            


@app.route("/channel", methods=["POST"])
def channelResults():
    channelName = request.form['channelName']
    videoToIndividualScores = {}
    videoIds = []
    videoScores = []
    allVideos = dm.get_channel_videos(channelName)
    ch = ioc.load_channel(channelName)
    if ch is None:
        ch = ioc.Channel(channelName, [])
        maxResults = 2
        for videoId in allVideos:
            score,individualScore = calculateVideoScore(videoId)
            if score is None:
                continue
            ch.videos.append(ioc.Video(videoId, videoId, score, individualScore))

            maxResults = maxResults-1
            if maxResults == 0:
                break
        ioc.cache_channel(ch)
    
    for video in ch.videos:
        videoIds.append(video.videoId)
        videoScores.append(video.score)
        videoToIndividualScores[video.videoId] = video.generate_statistics_pie();

    
    return render_template("channelPage.html", channelName=channelName.upper(),
                           barchart=ch.generate_statistics_bar(),
                           individualCharts=videoToIndividualScores,
                           channel=ch)


@app.route("/search", methods=["GET"])
def searchForm():
    return render_template("searchPage.html")
    
@app.route("/search", methods=["POST"])
def searchFormResults():
    score, individualScores = calculateVideoScore(request.form['videoId'])
    return render_template("searchPage.html", videoScore=score, pieHtml=dmMat.generate_pie(individualScores))



#main page of the application
@app.route("/")    
def index():
    
    return render_template("firstPage.html", a_variable = "teeest")
    

def calculateVideoScore(videoId):
    '''
    thsi method calls all the necessary functions to calculate the score
    a youtube video.
    1.Retrieving comments
    2.Tokenizing comments
    3.Lemmatizing comments
    4.clearing stop words from comments
    5.calculating the actual score
    '''
    start = time.time()
    comments = dm.retrieve_youtube_comments(videoId)
    print ("retrieved comments in : " + str(time.time() - start))
    start = time.time()    
    tokenComments = dm.tokenize(comments)
    print ("tokenized comments in : " + str(time.time() - start))
    start = time.time()  
    tokenLemmas = dm.lemmatize(tokenComments)
    print ("lemmatized comments in : " + str(time.time() - start))
    start = time.time()  
    cleanComments = dm.cleanStopWords(tokenLemmas)
    print ("cleaned comments in : " + str(time.time() - start))
    start = time.time()
    if len(cleanComments) == 0:
        return None, None
    score = dm.calculateScore(cleanComments, wordToRate)
    print ("score comments in : " + str(time.time() - start))
    return score

if __name__ == "__main__":
   app.run()