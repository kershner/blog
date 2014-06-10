import praw
import sys

count = 0
if len(sys.argv) < 2:
    # no command line options sent:
    print('Usage:')
    print('  python %s [subreddit]' % (sys.argv[0]))
    sys.exit()
target_subreddit = sys.argv[1]

print '\n\n\n\nGathering image URLs from /r/%s...' % target_subreddit
r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')

# Uncomment to scrape top results from year/month/all
submissions = r.get_subreddit(target_subreddit).get_hot(limit=50)
#submissions = r.get_subreddit(target_subreddit).get_top_from_year(limit=50)
#submissions = r.get_subreddit(target_subreddit).get_top_from_month(limit=50)
#submissions = r.get_subreddit(target_subreddit).get_top_from_all(limit=50)

file_object = open('url_log.txt', 'r+')
urls = list(file_object)

for submission in submissions:
    if submission.url + '\n' in urls:
        print '%s found in url_log.txt, skipping...' % submission.url
        pass
    elif '.gif' not in submission.url:
        print '%s not an image link, skipping...' % submission.url
        pass
    elif 'minus' in submission.url:
        print '%s from minus domain, skipping...' % submission.url
        pass
    elif 'gifsound' in submission.url:
        print '%s from gifsound domain, skipping...' % submission.url
        pass
    elif 'gifsoup' in submission.url:
        print '%s from gifsoup domain, skipping...' % submission.url
        pass
    elif '?' in submission.url:
        print '? found in URL, snipping and adding...'
        url_snip = submission.url.find('?')
        file_object.write(submission.url[:url_snip])
        file_object.write('\n')
        count += 1
    else:
        print '%s not found in url_log.txt, adding...' % submission.url
        file_object.write(submission.url)
        file_object.write('\n')
        count += 1

file_object.close()

number_of_gifs = len(urls)

print '\n\n%d GIFs added' % count
print 'Total number of GIFs: %d' % (number_of_gifs + count)

