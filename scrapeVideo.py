from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import os
import pyimgur
import secret
from stabVid import VideoBrokenException
import json

# imageio.mimsave(args.output + '.gif', ARR_ARR, fps=$FRAMESPERSECOND)


max_vid_length = 30

imgur = pyimgur.Imgur(secret.imgur_id)

user_agent = None


class VideoNotFoundException(Exception):
    pass


def extract_video_url(page_url):
    if page_url is None:
        raise VideoNotFoundException("No video found.")



    with urllib.request.urlopen(page_url) as response:
        info = response.info()

        if info.get_content_type() == "text/html":
            soup = BeautifulSoup(response, "html.parser")


            video_src = None

            try:
                video_src = soup.source["src"]

            except (AttributeError, KeyError):
                pass

            if not video_src:
                try:
                    video_src = soup.video["src"]

                except (AttributeError, KeyError):

                    pass

            if not video_src:
                raise VideoNotFoundException("No Video Found at " + page_url)


            if video_src.startswith("//"):
                video_src = "http:" + video_src


            return video_src
        return None


def get_streamable_url(url):

    parsed_uri = urllib.parse.urlparse(url)

    info_url = "https://api.streamable.com/videos" + parsed_uri.path

    with urllib.request.urlopen(url) as response:

        j = json.load(response)

        video_url = j['files']['mp4']['url']

        if video_url.startswith("//"):
            video_url = "https:" + video_url

        return video_url

def search_download_vid(submission, new_user_agent):
    global user_agent
    user_agent = new_user_agent


    submission_url = submission.url










