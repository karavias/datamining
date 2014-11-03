import webapp2
import gdata.youtube.service 
from nltk import word_tokenize

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        yts = gdata.youtube.service.YouTubeService() 
        urlpattern = 'http://gdata.youtube.com/feeds/api/videos/' + self.request.get("u") + '/comments?start-index=%d&max-results=25' 
        print(urlpattern)
        index = 1 
        url = urlpattern % index 
        comments = [] 
        while url: 
            ytfeed = yts.GetYouTubeVideoCommentFeed(uri=url) 
            #print (ytfeed)
            comments.extend([ word_tokenize(comment.content.text) for comment in ytfeed.entry ])
            print("comments? " + str(len(comments)))  
            #print (ytfeed.GetNextLink())
            if (not hasattr(ytfeed.GetNextLink(), 'href')):
                break;
            url = ytfeed.GetNextLink().href 
        for comment in comments:
            self.response.write(":::comment:::")
            self.response.write(comment)   
            self.response.write("\n")
        

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
