import praw
import urllib
from datetime import datetime


# Function to determine size of URL via HTML header data
def getsize(uri):
    image_file = urllib.urlopen(uri)
    size = image_file.headers.get("content-length")
    image_file.close()
    if size is None:
        return 'None'
    else:
        return int(size)


# Consolidate individual subreddit URL files into main file
def consolidate(category, target_subreddit):
    animals_urls = open('e:/programming/projects/blog/app/templates/pi_display/%s_urls.txt' % category, 'a+')
    animals_list = list(animals_urls)

    file_object = open('e:/programming/projects/blog/app/templates/pi_display/%s_urls.txt' % target_subreddit, 'a+')
    file_object_list = list(file_object)

    for url in file_object_list:
        if url in animals_list:
            continue
        else:
            print 'URL not found in main list, adding...'
            animals_urls.write(url)

    animals_urls.close()
    file_object.close()
    with open('e:/programming/projects/blog/app/templates/pi_display/%s_urls.txt' % category, 'r') as e:
        print 'Total number of GIFs in %s.txt: %d' % (category, len(list(e)))


def scrape(target_subreddit):
    def log():
        # Logs files being added and total number of GIFs to /reddit_scraper_log.txt
        time = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))
        log_data = '\n\n%d gifs added from /r/%s at %s.' % (count, target_subreddit, time)
        skipped = '\n%d bad links and %d large GIFs skipped.' % (bad_urls, large_urls)
        number_of_gifs = 'Total number of GIFs: %d' % (len(urls_list) + count)
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
    #submissions = r.get_subreddit(target_subreddit).get_top_from_all(limit=100)

    # Opening files, converting to Python lists
    urls_file = open('e:/programming/projects/blog/app/templates/pi_display/%s_urls.txt' % target_subreddit, 'a+')
    urls_list = list(urls_file)
    bad_urls_file = open('e:/programming/projects/blog/app/templates/pi_display/bad_urls.txt', 'a+')
    bad_urls_list = list(bad_urls_file)
    large_urls_file = open('e:/programming/projects/blog/app/templates/pi_display/large_urls.txt', 'a+')

    # Going through reddit submissions from the specified subreddit
    for submission in submissions:
        # Skip the URL if there is an error with the connection
        try:
            r = urllib.urlopen(submission.url)
        except:
            print 'Error requesting %s, skipping...' % submission.url
            continue
        # Already in urls.txt
        if submission.url + '\n' in urls_list:
            continue
        # Known bad URL
        elif submission.url + '\n' in bad_urls_list:
            continue
        # This URL throws a timeout error I don't know how to catch yet
        elif submission.url == 'http://www.picsarus.com/53FBHN.gif':
            continue
        # Not a .gif file
        if '.gif' not in submission.url:
            print '%s is not a GIF file, skipping...' % submission.url
            bad_urls_file.write(submission.url + '\n')
            bad_urls += 1
            continue
        # 404 status code is a broken link
        elif r.getcode() == 404:
            print '%s is a broken link, skipping...' % submission.url
            # Logging bad URL
            bad_urls_file.write(submission.url + '\n')
            bad_urls += 1
            continue
        # 302 is redirection, meaning bad link
        elif r.getcode() == 302:
            print '%s is a broken link, skipping...' % submission.url
            # Logging bad URL
            bad_urls_file.write(submission.url + '\n')
            bad_urls += 1
            continue
        # Don't want gifsound links
        elif 'sound' in submission.url:
            print '%s is a gifsound link, skipping...' % submission.url
            bad_urls_file.write(submission.url + '\n')
            bad_urls += 1
            continue
        try:
            if getsize(submission.url) == 'None':
                print '%s has no length data in HTTP header, adding...' % submission.url
                urls_file.write(str(submission.url) + '\n')
                continue
            # Imgur 'removed' image is 503 bytes
            elif getsize(submission.url) == 503:
                print '%s is a broken link, skipping...' % submission.url
                urls_file.write(str(submission.url) + '\n')
                bad_urls += 1
                continue
            # The Pi has a hard time with GIFs larger than 8MBs
            elif getsize(submission.url) > 8192000:
                print '%s is larger than 8MBs, skipping...' % submission.url
                large_urls_file.write(str(submission.url) + '\n')
                large_urls += 1
                continue
        except IOError:
            print 'Error reading HTTP header, skipping...'
            continue
        else:
            print '%s not found in %s_urls.txt, adding...' % (submission.url, target_subreddit)
            urls_file.write(submission.url)
            urls_file.write('\n')
            count += 1

    urls_file.close()
    bad_urls_file.close()
    large_urls_file.close()

    log()

# Category: Animals
scrape('aww_gifs')
scrape('awwgifs')
scrape('AnimalGIFs')
scrape('CatGifs')
scrape('slothgifs')
scrape('Puggifs')

consolidate('animals', 'aww_gifs')
consolidate('animals', 'awwgifs')
consolidate('animals', 'AnimalGIFs')
consolidate('animals', 'CatGifs')
consolidate('animals', 'slothgifs')
consolidate('animals', 'Puggifs')

# Category: Weird
scrape('wtf_gifs')
scrape('SurrealGifs')
scrape('creepy_gif')

consolidate('weird', 'wtf_gifs')
consolidate('weird', 'SurrealGifs')
consolidate('weird', 'creepy_gif')

# Category: Gaming
scrape('gaming_gifs')
scrape('gaming')
scrape('GamePhysics')

consolidate('gaming', 'gaming_gifs')
consolidate('gaming', 'gaming')
consolidate('gaming', 'GamePhysics')

# Category: Interesting/Educational
scrape('physicsgifs')
scrape('mechanical_gifs')
scrape('SpaceGifs')
scrape('interestinggifs')
scrape('EducationalGifs')
scrape('chemicalreactiongifs')

consolidate('educational', 'physicsgifs')
consolidate('educational', 'mechanical_gifs')
consolidate('educational', 'SpaceGifs')
consolidate('educational', 'interestinggifs')
consolidate('educational', 'EducationalGifs')
consolidate('educational', 'chemicalreactiongifs')