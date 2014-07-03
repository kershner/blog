import praw
import urllib2

target_subreddit = 'blackpeoplegifs'

r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')
submissions = r.get_subreddit(target_subreddit).get_hot(limit=50)

for submission in submissions:
    url = urllib2.urlopen(submission.url)
    print url.getcode()