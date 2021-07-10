import requests
import urllib.request
import os

import ytup
import auth

#   DOWNLOAD CLIP FROM TWICH
def twichdl(post):
    # https://github.com/kirovtome/python-api-twitch-clips/blob/master/dltwitchclips.py
    slug = post.url.rpartition('/')[-1]
    basepath = './videos/'

    clip_info = requests.get("https://api.twitch.tv/kraken/clips/" + slug, headers={"Client-ID": auth.twich_id, "Accept":"application/vnd.twitchtv.v5+json"}).json()
    try:
        thumb_url = clip_info['thumbnails']['medium']
    except:
        return
    mp4_url = thumb_url.split("-preview",1)[0] + ".mp4"
    out_filename = post.title + ".mp4"
    output_path = (basepath + out_filename)
    try:
        urllib.request.urlretrieve(mp4_url, output_path)
        print("downloaded from twich")
    except:
        print("Could not download die to error")

#   UPLOAD VIDEO TO YOUTUBE
def tubeup(post):
    ytup.uploadmp4(post)

#   CREATE FILE OBJECT TO STORE POSTED VIDEOS
posted = open('history.txt', 'r+')
readfile = posted.read()

#   MANAGE DIRECTORY
directory = 'videos'
path = os.path.join('.', directory)
if not os.path.isdir(path):
    os.mkdir(path)

#   GET HOTTEST POSTS FROM R/LIVESTREAMFAIL
hot_posts = auth.reddit.subreddit('livestreamfail').hot(limit=20)

#   MAIN LOOP
for post in hot_posts:
    
    #   CHECK IF CLIP HAS ALREADY BEEN POSTED BEFORE
    if post.url in readfile:
        print("present")
        continue
    
    #   ONLY GO THROUGH  TWICH CLIPS
    if post.url.startswith("https://clips.twitch.tv/"):
        
        print("==============================")
        print(post.title + " || " + post.link_flair_text.split(' ')[1])
        print(post.url + "\n")
        
        twichdl(post)
        tubeup(post)
        
        try:
            os.remove("videos/" + post.title + ".mp4")
        except:
            print("file not present")
        
        #   ADD POST URL TO FILE
        posted.write(post.url + "\n")

        