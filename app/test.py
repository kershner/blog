import praw

r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')
submissions = r.get_subreddit('reactiongifs').get_hot(limit=25)

for submission in submissions:
    print submission.url
    print '.gif' in submission.url