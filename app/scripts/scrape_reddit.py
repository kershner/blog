import praw
import sys
import urllib
from datetime import datetime


# Function to determine size of URL via HTML header data
def getsize(uri):
    image_file = urllib.urlopen(uri)
    size = image_file.headers.get("content-length")
    image_file.close()
    return int(size)


def log():
    # Logs files being added and total number of GIFs to /reddit_scraper_log.txt
    time = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))
    log_data = '\n\nAdded %d gifs from /r/%s at %s.' % (count, target_subreddit, time)
    removed = '\n%d bad links removed' % bad_urls
    number_of_gifs = '\nTotal number of GIFs: %d' % (len(urls) + count)
    with open('/home/tylerkershner/app/templates/pi_display/reddit_scraper_log.txt', 'a') as log_file:
        log_file.write(log_data)
        log_file.write(removed)
        log_file.write(number_of_gifs)
    print log_data
    print removed
    print number_of_gifs

# Variables to keep track of certain GIFs added
count = 0
bad_urls = 0

if len(sys.argv) < 2:
    # no command line options sent:
    print('Usage:')
    print('  python %s [subreddit]' % (sys.argv[0]))
    sys.exit()

target_subreddit = sys.argv[1]

print '\n\n\n\nGathering image URLs from /r/%s...' % target_subreddit

# Accessing Reddit API
r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')

# Uncomment to scrape top results from year/month/all
submissions = r.get_subreddit(target_subreddit).get_hot(limit=50)
#submissions = r.get_subreddit(target_subreddit).get_top_from_year(limit=50)
#submissions = r.get_subreddit(target_subreddit).get_top_from_month(limit=50)
#submissions = r.get_subreddit(target_subreddit).get_top_from_all(limit=50)

# Opening list of URLs in read + write mode
file_object = open('/home/tylerkershner/app/templates/pi_display/urls.txt', 'r+')

# Converting text file to list object to more easily perform operations on it
urls = list(file_object)

for submission in submissions:
    # First 6 statments determine which URLs to skip
    try:
        if submission.url + '\n' in urls:  # Already in urls.txt
            pass
        elif '.gif' not in submission.url:  # Not a .gif file
            pass
        elif getsize(submission.url) == 503:  # Imgur 'removed' image is 503 bytes
            # Logging bad URL
            with open('/home/tylerkershner/app/templates/pi_display/bad_urls.txt', 'a') as f:
                f.write(submission.url + '\n')
            bad_urls += 1
            pass
        # Some imgur URLs have a ? at the end, here we write the URL up to the ?
        elif '?' in submission.url:
            print '? found in URL, snipping and adding...'
            url_snip = submission.url.find('?')
            file_object.write(submission.url[:url_snip])
            file_object.write('\n')
            count += 1
        else:
            print '%s not found in urls.txt, adding...' % submission.url
            file_object.write(submission.url)
            file_object.write('\n')
            count += 1
    except UnicodeError:
        pass

file_object.close()

log()