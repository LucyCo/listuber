#
#
#
#
# # from flask import Flask
# # from config import DEBUG_KEY, get_config
# import webapp2
# #
# #
# # YOUTUBE_API_SERVICE_NAME = "youtube"
# # YOUTUBE_API_VERSION = "v3"
# #
# #
# # app = Flask(__name__)
# #
# #
# # @app.route("/")
# # def hello():
# #     return "Hello ho"
# # try to send a search request to youtube using python
#
#
# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         self.response.write("Hello")
#
#
# app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
# def main():
#     from paste import httpserver
#     httpserver.serve(app, host='127.0.0.1', port='8080')
# # def main():
# #     app.run()
#
# if __name__=='__main__':
#     main()
#
# #
# # if __name__ == "__main__":
# #     app.run(debug=get_config(DEBUG_KEY))

# import os
# import urllib
# import webapp2
# from paste import httpserver
# import jinja2
# from config import DEBUG_KEY, API_KEY_KEY, get_config
# from googleapiclient.discovery import build
# from optparse import OptionParser
#
# JINJA_ENVIRONMENT = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#     extensions=['jinja2.ext.autoescape'])
#
# # Set DEVELOPER_KEY to the "API key" value from the Google Developers Console:
# # https://console.developers.google.com/project/_/apiui/credential
# # Please ensure that you have enabled the YouTube Data API for your project.
# DEVELOPER_KEY = get_config(API_KEY_KEY)
# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"
#
#
# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         if DEVELOPER_KEY == "REPLACE_ME":
#             self.response.write("""You must set up a project and get an API key
#                                  to run this project.  Please visit
#                                  <landing page> to do so.""")
#         else:
#             youtube = build(
#                 YOUTUBE_API_SERVICE_NAME,
#                 YOUTUBE_API_VERSION,
#                 developerKey=DEVELOPER_KEY)
#             search_response = youtube.search().list(
#                 q="Hello",
#                 part="id,snippet",
#                 maxResults=5
#             ).execute()
#
#             videos = []
#             channels = []
#             playlists = []
#
#             for search_result in search_response.get("items", []):
#                 if search_result["id"]["kind"] == "youtube#video":
#                     videos.append("%s (%s)" % (search_result["snippet"]["title"],
#                                        search_result["id"]["videoId"]))
#                 elif search_result["id"]["kind"] == "youtube#channel":
#                     channels.append("%s (%s)" % (search_result["snippet"]["title"],
#                                          search_result["id"]["channelId"]))
#                 elif search_result["id"]["kind"] == "youtube#playlist":
#                     playlists.append("%s (%s)" % (search_result["snippet"]["title"],
#                                           search_result["id"]["playlistId"]))
#
#             template_values = {
#                 'videos': videos,
#                 'channels': channels,
#                 'playlists': playlists
#             }
#
#             self.response.headers['Content-type'] = 'text/plain'
#             template = JINJA_ENVIRONMENT.get_template('index.html')
#             self.response.write(template.render(template_values))
#
# app = webapp2.WSGIApplication([('/.*', MainHandler)], debug=get_config(DEBUG_KEY))
#
#
# def main():
#         httpserver.serve(app, host='127.0.0.1', port='8080')
#         app.run()
#
#
# if __name__ == '__main__':
#     main()
#
#
#!/usr/bin/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCG_5q4O9wxy-b69WccOaXjUz4lPDNqcoI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(q=options.q, part="id,snippet", maxResults=options.max_results).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

    print "Videos:\n", "\n".join(videos), "\n"
    print "Channels:\n", "\n".join(channels), "\n"
    print "Playlists:\n", "\n".join(playlists), "\n"


if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()

    try:
        print args
        youtube_search(args)
    except Exception, e:
        print "An HTTP error %s occurred:\n%s" % (e.message, e.args)
