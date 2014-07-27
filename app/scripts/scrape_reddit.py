import praw
import urllib2
from datetime import datetime


# Creating Gif class to hold count data
class Gif(object):
    def __init__(self, count):
        self.count = count

    def counter(self):
        self.count += 1

# Instantiating Gif class
gif = Gif(0)


def scrape_reddit(target_subreddit, path):
    # Function to determine size of URL via HTTP header data
    def getsize(url):
        url = urllib2.urlopen(url)
        try:
            size = int(url.info()['content-length'])
            return size
        except KeyError:
            print '%s has no content-length data in HTTP header, skipping...' % submission.url
            return 'None'

    # Logs files being added and total number of GIFs to /reddit_scraper_log.txt
    def log():
        time = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))
        log_data = '\n\n%d gifs added from /r/%s at %s.' % (count, target_subreddit, time)
        skipped = '\n%d bad links and %d large GIFs skipped.' % (bad_urls, large_urls)
        number_of_gifs = 'Total number of GIFs: %d' % (len(urls_list) + count)
        with open('%s/reddit_scraper_log.txt' % path, 'a') as logfile:
            logfile.write(log_data)
            logfile.write(skipped)
            logfile.write(number_of_gifs)
        print log_data
        print skipped
        print number_of_gifs

    # Variables to keep track of certain GIFs added
    count = 0
    bad_urls = 0
    large_urls = 0

    print '\n\n\n\nGathering image URLs from /r/%s...' % target_subreddit

    # Accessing Reddit API
    r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')

    # Uncomment to scrape top results from year/month/all
    submissions = r.get_subreddit(target_subreddit).get_hot(limit=50)
    #submissions = r.get_subreddit(target_subreddit).get_top_from_year(limit=50)
    #submissions = r.get_subreddit(target_subreddit).get_top_from_month(limit=50)
    #submissions = r.get_subreddit(target_subreddit).get_top_from_all(limit=50)

    # Opening files, converting to Python lists
    urls_file = open('%s/urls.txt' % path, 'a+')
    urls_list = list(urls_file)
    bad_urls_file = open('%s/bad_urls.txt' % path, 'a+')
    bad_urls_list = list(bad_urls_file)
    large_urls_file = open('%s/large_urls.txt' % path, 'a+')
    large_urls_list = list(large_urls_file)

    # Going through reddit submissions from the specified subreddit
    for submission in submissions:
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
        elif not submission.url.endswith('.gif'):
            print '%s is not a GIF file, skipping...' % submission.url
            bad_urls_file.write(str(submission.url) + '\n')
            bad_urls += 1
            continue
        # Don't want gifsound links
        elif 'sound' in submission.url:
            print '%s is a gifsound link, skipping...' % submission.url
            bad_urls_file.write(str(submission.url) + '\n')
            bad_urls += 1
            continue
        # This URL causes an ASCII -> Unicode error
        elif 'Von_Karman' in submission.url:
            bad_urls += 1
            continue
        try:
            r = urllib2.urlopen(submission.url)
        except (urllib2.HTTPError, urllib2.URLError):
            bad_urls += 1
            print '%s returns 403 forbidden or timed out, skipping...' % submission.url
            bad_urls_file.write(str(submission.url) + '\n')
            continue
        # 404 status code is a broken link
        if r.getcode == 404:
            print '%s is a broken link (404), skipping...' % submission.url
            # Logging bad URL
            bad_urls_file.write(str(submission.url) + '\n')
            bad_urls += 1
            continue
        # 302 is redirection, meaning bad link
        elif r.getcode == 302:
            print '%s is a broken link (302), skipping...' % submission.url
            # Logging bad URL
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
            large_urls_file.write(str(submission.url) + '\n')
            large_urls += 1
            continue
        # Imgur 'removed' image is 503 bytes
        elif getsize(submission.url) == 503:
            print '%s is a broken link (503 bytes), skipping...' % submission.url
            bad_urls_file.write(str(submission.url) + '\n')
            bad_urls += 1
            continue
        else:
            print '%s not found in urls.txt, adding...' % submission.url
            urls_file.write(str(submission.url) + '\n')
            count += 1
            gif.counter()

    urls_file.close()
    bad_urls_file.close()
    large_urls_file.close()

    log()

subreddits = ['gifs', 'gif', 'blackpeoplegifs', 'SpaceGifs', 'physicsgifs', 'educationalgifs', 'chemicalreactiongifs',
              'SurrealGifs', 'Puggifs', 'slothgifs', 'asianpeoplegifs', 'gaming_gifs', 'Movie_GIFs', 'funnygifs',
              'wheredidthesodago', 'reactiongifs', 'creepy_gif', 'perfectloops', 'aww_gifs', 'AnimalsBeingJerks',
              'AnimalGIFs', 'whitepeoplegifs', 'interestinggifs', 'cinemagraphs', 'wtf_gifs',
              'MichaelBayGifs', 'naturegifs', 'pugs', 'gaming', 'Wastedgifs', 'GamePhysics', 'catgifs',
              'opticalillusions', 'wrestlinggifs']

if __name__ == '__main__':
    prompt = raw_input('Are you scraping from work or home? > ').lower()
    if prompt == 'work':
        current_path = 'E:/programming/projects/blog/app/templates/pi_display/logs/'
    elif prompt == 'home':
        current_path = 'H:/programming/projects/blog/app/templates/pi_display/logs/'

    time_start = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))

    for subreddit in subreddits:
        scrape_reddit(subreddit, current_path)

    time_end = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))

    print 'reddit scrape began at %s' % time_start
    print 'reddit scrape finished at %s' % time_end
    print '%d GIFs added.' % gif.count