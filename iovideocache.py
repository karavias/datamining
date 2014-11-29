'''
iovideocache module
This module implements the methods for caching
channel statistics in files and loading them back
'''
import pickle
#from cStringIO import StringIO
import os
import dm_matLib as dmMat
from pandas import DataFrame, set_option, Series
import time

class Video(object):
    '''
    class to host the video analytics
    which are the name, the score, and the individual scores
    '''
    def __init__(self, video_attributes, mean_score, individual_scores):
        print video_attributes
        self.video_id = video_attributes["id"]
        self.title = video_attributes["title"]
        self.score = mean_score
        self.individual_scores = individual_scores
        self.url = video_attributes["url"]
        self.image = video_attributes["image"]
        self.date = video_attributes["time"]
        print self

    def generate_statistics_pie(self):
        '''
        generate pie chart representing the rate distribution
        '''
        return dmMat.generate_pie(self.individual_scores)

    def generate_image_url(self):
        '''
        Generates the html code with the image for the video
        '''
        return "<img src='" + self.image + "' style='width:200px;height:150px;'/>"

    def generate_href(self):
        '''
        Generates the html code with the url for the video
        '''
        return "<a href='" + self.url + "'>" + self.title + "</a>"

class Channel(object):
    '''
    class to host the channel analytics which are
    the name of the channel and a list of video analytics
    '''
    def __init__(self, name, videos_statistics):
        self.name = name
        self.videos = videos_statistics

    def generate_statistics_bar(self):
        '''
        generate the bar chart representing the history scores
        '''
        print(str([video.score for video in self.videos]))
        print(str([video.video_id for video in self.videos]))
        return dmMat.generate_histogram([video.score for video in self.videos],\
                                        [video.video_id for video in self.videos])

    def generate_table(self):
        '''
        generate overall statistics
        '''
        data = {}
        set_option('display.max_colwidth', -1)
        for video in self.videos:

            data[time.strftime("%B %d, %Y", video.date)] = Series([video.generate_href(),\
                video.score,\
                video.image.generate_image_url(),\
                remove_comments(video.generate_statistics_pie()).replace('\n', ' ')],\
                index=["Title", "Score", "Image", "Score Distribution"])
        return DataFrame(data).T.to_html(escape=False)



def cache_channel(channel):
    '''
    cache channel analytics into a file
    '''
    pickle.dump(channel, open('cache/' + channel.name, 'wb'))


def load_channel(name):
    '''
    Try to load channel analytics
    if channel doesn't exist, then return None
    '''
    if os.path.isfile('cache/' + name):
        return pickle.load(open('cache/' + name, 'rb'))
    return None


def remove_comments(text):
    '''
    Removes comments from strings that contain
    '''
    text = text.splitlines(True)
    out = ""
    for line in text:
        print line
        out = out + line.split("//")[0]
    return out


if __name__ == "__main__":
    CHANNEL_ = load_channel("smosh")
    print CHANNEL_.generate_table()
