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

APP_ = Flask(__name__)
WORLD_TO_RATE = dm.read_sentiment_dictionary()


@APP_.route("/channel", methods=["POST"])
def channel_results():
    """Handler that returns the request for the channels statistics."""
    channel_name = request.form['channelName']
    print channel_name
    channel = ioc.load_channel(channel_name)
    if channel is None:
        channel = ioc.Channel(channel_name, [])
        max_results = 2
        all_videos = youtools.get_channel_videos(channel_name)
        for video_attributes in all_videos:
            score, individual_score =\
                calculate_video_score(video_attributes["id"])
            if score is None:
                continue
            channel.videos.append(ioc.Video(video_attributes,\
                                score, individual_score))

            max_results = max_results-1
            if max_results == 0:
                break
        ioc.cache_channel(channel)
    return render_template("channelPage.html", channel=channel)


@APP_.route("/search", methods=["GET"])
@APP_.route("/")
def search_form():
    """Simple page that displays the search options."""
    return render_template("searchPage.html")

@APP_.route("/search", methods=["POST"])
def search_form_results():
    """Handler that returns the request for the video statistics."""
    video_id = request.form["videoUrl"].split("v=")[1].split("&")[0]
    score, individual_scores = calculate_video_score(video_id)
    return render_template("searchPage.html", videoScore=score,\
        pieHtml=dm_plot.generate_pie(individual_scores))




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
    token_lemmas = dm.lemmatize(token_comments)
    clean_comments = dm.clean_stop_words(token_lemmas)
    if len(clean_comments) == 0:
        return None, None
    score = dm.calculate_score(clean_comments, WORLD_TO_RATE)
    return score

if __name__ == "__main__":
    APP_.run(debug=True)
