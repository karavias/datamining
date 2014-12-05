"""
youflask Module.

Implements the web application that handles
the user's requests
"""

from flask import Flask, request, \
     render_template
import dm_lib as dm
import iovideocache as ioc
import dm_plotlib as dm_plot
import dm_youtools as youtools
import lib_speed as ls


APP_ = Flask(__name__)
WORLD_TO_RATE = dm.read_sentiment_dictionary()

@ls.reset_calculate
@APP_.route("/channel", methods=["POST"])
def channel_results():
    """Handler that returns the request for the channels statistics."""
    channel_name = request.form['channelName']
    channel = ioc.load_channel(channel_name)
    if channel is None:
        channel = ioc.Channel(channel_name, [])

        all_videos = youtools.get_channel_videos(channel_name)
        count = 0
        #calculate the score for only the 5 first videos
        #to ensure the time will be acceptable
        for index in range(min(5, len(all_videos))):
            video_attributes = all_videos[index]
            count = count + 1
            score, individual_score =\
                calculate_video_score(video_attributes["id"])
            if score is None:
                continue
            channel.videos.append(ioc.Video(video_attributes,\
                                score, individual_score))

        ioc.cache_channel(channel)
    return render_template("channelPage.html", channel=channel,\
                    stats=ls.get_speed_means())

@ls.reset_calculate
@APP_.route("/search", methods=["GET"])
@APP_.route("/")
def search_form():
    """Simple page that displays the search options."""
    return render_template("searchPage.html")

@ls.reset_calculate
@APP_.route("/search", methods=["POST"])
def search_form_results():
    """Handler that returns the request for the video statistics."""
    video_id = request.form["videoUrl"].split("v=")[1].split("&")[0]
    score, individual_scores = calculate_video_score(video_id)
    return render_template("searchPage.html", videoScore=score,\
        pieHtml=dm_plot.generate_pie(individual_scores))


@ls.speed_calculate
def calculate_video_score(video_id):
    """
    Calculate the sentiment score for the youtube video.

    1.Retrieving comments
    2.Tokenizing comments
    3.Lemmatizing comments
    4.clearing stop words from comments
    5.calculating the actual score

    Keyword arguments:
    video_id -- a string representing the video id
    """
    comments = youtools.retrieve_youtube_comments(video_id)
    token_comments = dm.tokenize(comments)
    clean_comments = dm.clean_stop_words(token_comments)
    if len(clean_comments) == 0:
        return None, None
    score = dm.calculate_score(clean_comments, WORLD_TO_RATE)

    return score



if __name__ == "__main__":
    APP_.run(debug=True)

