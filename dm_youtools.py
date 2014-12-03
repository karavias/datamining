"""
dm_youtools module.

This module contains the methods required for retrieving data from youtube.
"""
import gdata.youtube.service
import time
import urllib, json
import socket

def retrieve_youtube_comments(video_id):
    """
    Retrieve youtube comments for the given video.

    Keyword arguments:
    video_id -- the video for which we want to retrieve the comments
    """
    yts = gdata.youtube.service.YouTubeService()
    index = 1
    urlpattern = 'http://gdata.youtube.com/feeds/api/videos/' + video_id +\
                '/comments?start-index=%d&max-results=50'
    url = urlpattern % index
    comments = []
    while url:
        try:
            ytfeed = yts.GetYouTubeVideoCommentFeed(uri=url)
        except (socket.gaierror, gdata.service.RequestError):
            break
        comments.extend([comment.content.text for comment in ytfeed.entry])
        print (str(len(comments)))        
        if not hasattr(ytfeed.GetNextLink(), 'href'):
            break
        url = ytfeed.GetNextLink().href
    return comments


def get_channel_videos(author):
    """
    Retrieve channel's videos basic information.

    Keyword arguments:
    author -- the name of the channel
    """
    found_all = False
    ind = 1
    videos = []
    while not found_all:
        inp = urllib.urlopen((r'http://gdata.youtube.com/feeds/api/videos?'+\
            'start-index={0}&max-results=50&alt=json&orderby=published&'+\
            'author={1}').format(ind, author))
        try:
            resp = json.load(inp)
            inp.close()
            returned_videos = resp['feed']['entry']
            for video in returned_videos:
                videos.append(video)

            ind += 50
            print len(videos)
            if len(returned_videos) < 50:
                found_all = True
        except:
            #catch the case where the number of videos in the channel is a
            #multiple of 50
            print "error"
            found_all = True
    out = []
    for video in videos:
        out.append({"id":video["id"]["$t"].split('videos/')[1],\
                "title":video['title']['$t'],\
                "url":video['media$group']['media$player'][0]['url'],\
                "image":video['media$group']['media$thumbnail'][0]['url'],\
                "time":time.strptime(video["published"]["$t"].split(".")[0],\
                "%Y-%m-%dT%H:%M:%S")})

    return out
