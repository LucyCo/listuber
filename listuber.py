#!/usr/bin/python
from googleapiclient.discovery import build
from flask import Flask, request
import config
app = Flask(__name__)


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = config.get_config(config.API_KEY_KEY)
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


@app.route('/')
def display():
    return "Looks like it works!"


@app.route('/youtube_search', methods=['GET', 'POST'])
def youtube_search():
    keyword = request.args.get('keyword')
    num_results = request.args.get('num_results')
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(q=keyword, part="id,snippet", maxResults=num_results).execute()

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
    return videos


if __name__ == "__main__":
    app.run(debug=config.get_config(config.DEBUG_KEY), port=3134)
