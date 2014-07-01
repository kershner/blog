import praw
import sys
import requests
from datetime import datetime


# Function to determine size of URL via HTML header data
def getsize(url):
    try:
        r = requests.get(url, stream=True)
        size = int(r.headers['content-length'])
        return size
    except KeyError:
        return 'None'


# Logs files being added and total number of GIFs to /reddit_scraper_log.txt
def log():
    time = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))
    log_data = '\n\n%d gifs added from /r/%s at %s.' % (count, target_subreddit, time)
    skipped = '\n%d bad links and %d large GIFs skipped.' % (bad_urls, large_urls)
    number_of_gifs = 'Total number of GIFs: %d' % (len(urls_list) + count)
    with open('/home/tylerkershner/app/templates/pi_display/reddit_scraper_log.txt', 'a') as log_file:
        log_file.write(log_data)
        log_file.write(skipped)
        log_file.write(number_of_gifs)
    print log_data
    print skipped
    print number_of_gifs

# Variables to keep track of certain GIFs added
count = 0
bad_urls = 0
large_urls = 0

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

# Opening files, converting to Python lists
urls_file = open('/home/tylerkershner/app/templates/pi_display/urls.txt', 'a+')
urls_list = list(urls_file)
bad_urls_file = open('/home/tylerkershner/app/templates/pi_display/bad_urls.txt', 'a+')
bad_urls_list = list(bad_urls_file)
large_urls_file = open('/home/tylerkershner/app/templates/pi_display/large_urls.txt', 'a+')
large_urls_list = list(large_urls_file)

# Going through reddit submissions from the specified subreddit
for submission in submissions:
    # Skip the URL if there is an error with the connection
    try:
        r = requests.get(submission.url)
    except:
        print 'Error requesting %s, skipping...' % submission.url
        continue
    # Already in urls.txt
    if submission.url + '\n' in urls_list:
        continue
    # Known bad URL
    elif submission.url + '\n' in bad_urls_list:
        bad_urls += 1
        continue
    # Known Large URL
    elif submission.url + '\n' in large_urls_list:
        large_urls += 1
        continue
    # Not a .gif file
    if '.gif' not in submission.url:
        print '%s is not a GIF file, skipping...' % submission.url
        bad_urls_file.write(str(submission.url) + '\n')
        bad_urls += 1
        continue
    # 404 status code is a broken link
    if r.status_code == 404:
        print '%s is a broken link (404), skipping...' % submission.url
        # Logging bad URL
        bad_urls_file.write(str(submission.url) + '\n')
        bad_urls += 1
        continue
    # 302 is redirection, meaning bad link
    if r.status_code == 302:
        print '%s is a broken link (302), skipping...' % submission.url
        # Logging bad URL
        bad_urls_file.write(str(submission.url) + '\n')
        bad_urls += 1
        continue
    # Don't want gifsound links
    if 'sound' in submission.url:
        print '%s is a gifsound link, skipping...' % submission.url
        bad_urls_file.write(str(submission.url) + '\n')
        bad_urls += 1
        continue
    # If the getsize function returned None, there was an error
    if getsize(submission.url) == 'None':
        print '%s has no length data in HTTP header, skipping...' % submission.url
        bad_urls_file.write(str(submission.url) + '\n')
        bad_urls += 1
        continue
    # The Pi has a hard time with GIFs larger than 8MBs
    elif getsize(submission.url) > 8192000:
        print '%s is larger than 8MBs, skipping...' % submission.url
        continue
    # Imgur 'removed' image is 503 bytes
    elif getsize(submission.url) == 503:
        print '%s is a broken link (503 bytes), skipping...' % submission.url
        urls_file.write(str(submission.url) + '\n')
        bad_urls += 1
        continue
    else:
        print '%s not found in urls.txt, adding...' % submission.url
        urls_file.write(str(submission.url) + '\n')
        count += 1

urls_file.close()
bad_urls_file.close()
large_urls_file.close()


log()