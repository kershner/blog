import praw
import sys

if len(sys.argv) < 2:
    # no command line options sent:
    print('Usage:')
    print('  python %s [subreddit]' % (sys.argv[0]))
    sys.exit()
target_subreddit = sys.argv[1]

print 'Gathering image URLs from /r/%s...' % target_subreddit
r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')
submissions = r.get_subreddit(target_subreddit).get_hot(limit=25)
file_object = open('url_log.txt', 'r+')
urls = list(file_object)

for submission in submissions:
    if submission.url + '\n' in urls:
        print '%s found in url_log.txt, skipping...' % submission.url
        pass
    elif '.gif' not in submission.url:
        print '%s not an image link, skipping...' % submission.url
        pass
    elif '?' in submission.url:
        print '? found in URL, snipping and adding...'
        url_snip = submission.url.find('?')
        file_object.write(submission.url[:url_snip])
        file_object.write('\n')
    else:
        print '%s not found in url_log.txt, adding...' % submission.url
        file_object.write(submission.url)
        file_object.write('\n')


file_object.close()