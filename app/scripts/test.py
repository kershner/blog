import praw
import requests
import urllib

target_subreddit = 'gaming_gifs'

r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')

submissions = r.get_subreddit(target_subreddit).get_hot(limit=50)


def getsize(uri):
    image_file = urllib.urlopen(uri)
    size = image_file.headers.get("content-length")
    if size is None:
        image_file.close()
        return 'None'
    else:
        image_file.close()
        return (int(size) / 1024) / 1024


for submission in submissions:
    print '%s - %d MBs' % (submission.url, getsize(submission.url))