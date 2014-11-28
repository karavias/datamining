import pickle
from cStringIO import StringIO
import os
import dm_matLib as dmMat
from pandas import *

class Video:
    '''
    class to host the video analytics
    which are the name, the score, and the individual scores
    '''
    def __init__(self, videoId, title, meanScore, individualScores, url, image):
        self.videoId = videoId;
        self.title = title;
        self.score = meanScore;
        self.individualScores = individualScores;
        self.url = url
        self.image = image
    
    
    def generate_statistics_pie(self):
        '''
        generate pie chart representing the rate distribution
        '''
        return dmMat.generate_pie(self.individualScores)

class Channel:
    '''
    class to host the channel analytics which are
    the name of the channel and a list of video analytics
    '''
    def __init__(self, name, videosStatistics):
        self.name = name
        self.videos = videosStatistics
    
    def generate_statistics_bar(self):
        '''
        generate the bar chart representing the history scores
        '''
        return dmMat.generate_histogram([video.score for video in self.videos], 
                                        [video.videoId for video in self.videos])
    
    def generate_table(self):
        '''
        generate overall statistics
        '''
        data = {}
        for video in self.videos:
            data[video.videoId] = Series([video.title, video.score, video.image, video.url], index=["Title", "Score", "Image", "Url"])
        return DataFrame(data).T.to_html()
    
        
  
def cache_channel(ch):
    '''
    cache channel analytics into a file
    '''
    pickle.dump(ch, open('cache/' + ch.name, 'wb'))


def load_channel(name):
    '''
    Try to load channel analytics
    if channel doesn't exist, then return None
    '''
    if (os.path.isfile('cache/' + name)):
        return pickle.load(open('cache/' + name, 'rb'))
    return None




if __name__ == "__main__":
    '''
    vs = []
    vs.append(Video("name1", 4.5, [2.2, 4.3, 3], "", ""))
    vs.append(Video("name2", 4.5, [2.3, 3.3, 4], "", ""))
    vs.append(Video("name3", 4.5, [2.4, 2.3, 3], "", ""))
    vs.append(Video("name4", 4.5, [2.5, 4.3, 1], "", ""))
    cs = Channel(vs)
    src = StringIO()
    pickle.Pickler(src)
    pickle.dump(cs, open('cache/save.p', 'wb'))
    newData = pickle.load(open('cache/save.p', 'rb'))
    print newData.videos[1].name
    '''