from flask import Flask

import dm_lib

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
    return str(score)
    
  
    

if __name__ == "__main__":
    app.run()