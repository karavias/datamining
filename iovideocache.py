"""
iovideocache module.

The module implements the methods for caching
channel statistics in files and loading them back
"""
import pickle
#from cStringIO import StringIO
import os
import dm_plotlib as dm_plot
from pandas import DataFrame, set_option, Series
from time import mktime
from datetime import datetime
import re
import lib_speed as ls

class Video(object):

    """
    Class to host the video analytics.

    The video analytics are:
    -the name, the score, and the individual scores
    """

    def __init__(self, video_attributes, mean_score, individual_scores):
        """
        Constructor.

        Keyword arguments:
        video_attributes -- a dictionary with the basic info of a video
        mean_score -- the score of the video
        individual_scores -- a list with scores for videos
        """
        self.video_id = video_attributes["id"]
        self.title = video_attributes["title"]
        self.score = mean_score
        self.individual_scores = individual_scores
        self.url = video_attributes["url"]
        self.image = video_attributes["image"]
        self.date = video_attributes["time"]

    def generate_statistics_pie(self):
        """Generate pie chart representing the rate distribution."""
        return dm_plot.generate_pie(self.individual_scores)

    def generate_image_url(self):
        """Generate the html code with the image for the video."""
        return "<img src='" + self.image +\
                "' style='width:200px;height:150px;'/>"

    def generate_href(self):
        """Generate the html code with the url for the video."""
        return "<a href='" + self.url + "'>" + self.title + "</a>"

class Channel(object):

    """
    Class to host the channel analytics.

    The analytics are:
    -the name of the channel
    -list of video analytics
    """

    def __init__(self, name, videos_statistics):
        """Constructor.

        Keyword arguments:
        name -- The name of the channel
        videos_statistics -- A list of video objects
        """
        self.name = name
        self.videos = videos_statistics

    def generate_statistics_bar(self):
        """Generate the bar chart representing the history scores."""
        return dm_plot.generate_histogram(\
                    [datetime.fromtimestamp(mktime(video.date))\
                    for video in self.videos],\
                    [video.score for video in self.videos])

    def generate_table(self):
        """Generate overall statistics."""
        data = {}
        set_option('display.max_colwidth', -1)
        for video in self.videos:
#time.strftime("%B %d, %Y", video.date)
            data[datetime.fromtimestamp(mktime(video.date))] = \
                Series([video.generate_href(),\
                video.score,\
                video.generate_image_url(),\
                remove_comments(video.generate_statistics_pie()).\
                        replace('\n', '')],\
                index=["Title", "Score", "Image", "Score Distribution"])
        return DataFrame(data).T.to_html(escape=False)


@ls.speed_calculate
def cache_channel(channel):
    """Cache channel analytics into a file."""
    pickle.dump(channel, open('cache/' + channel.name, 'wb'))

@ls.speed_calculate
def load_channel(name):
    """
    Load channel analytics.

    If channel doesn't exist, then returns None
    """
    if os.path.isfile('cache/' + name):
        return pickle.load(open('cache/' + name, 'rb'))
    return None


@ls.speed_calculate
def remove_comments(string):
    """
    Remove comments from javascript code.

    Identifies /* */ and // comments and removes them correctly.
    Handles situation when these letters appear inside strings.
    """
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

