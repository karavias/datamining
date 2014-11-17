from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import dm_lib as dm

app = Flask(__name__)

@app.route("/search", methods=["GET"])
def searchForm():
    return render_template("searchPage.html")
    
@app.route("/search", methods=["POST"])
def searchFormResults():
    wordToRate = dm.read_sentiment_dictionary()            
    print(len(wordToRate))
    comments = dm.retrieve_youtube_comments("sRJOU0Fi9Ts")
    tokenComments = dm.tokenize(comments)
    print(tokenComments)
    tokenLemmas = dm.lemmatize(tokenComments)
    cleanComments = dm.cleanStopWords(tokenLemmas) 
    score = dm.calculateScore(cleanComments, wordToRate)
    return render_template("searchPage.html", videoScore=score)

    

#main page of the application
@app.route("/")    
def index():
    
    return render_template("firstPage.html", a_variable = "teeest")
    

if __name__ == "__main__":
    app.run()