from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import dm_lib as dm
import time
import dm_matLib as dmMat
app = Flask(__name__)
wordToRate = dm.read_sentiment_dictionary()            


@app.route("/channel", methods=["POST"])
def channelResults():
    channelName = request.form['channelName']
    videoToIndividualScores = {}
    data = {}
    videoIds = []
    videoScores = []
    allVideos = dm.get_channel_videos(channelName)
    maxResults = 2
    for videoId in allVideos:
        print videoId
        videoIds.append(videoId)
        score,individualScore = calculateVideoScore(videoId)
        videoScores.append(score)
        videoToIndividualScores[videoId] = dmMat.generate_pie(individualScore)
        maxResults = maxResults-1
        if maxResults == 0:
            break
    print videoIds
    return render_template("channelPage.html", channelName=channelName.upper(),
                           barchart=dmMat.generate_histogram(videoScores, videoIds),
                           individualCharts=videoToIndividualScores)


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
        return None    
    score = dm.calculateScore(cleanComments, wordToRate)
    print ("score comments in : " + str(time.time() - start))
    return score

if __name__ == "__main__":
    app.run()