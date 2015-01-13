import requests
from requests import exceptions
import praw


class Log(object):
    def __init__(self, all_gifs, animals_gifs, gaming_gifs, strange_gifs, educational_gifs, temp_count):
        self.all_gifs = all_gifs
        self.animals_gifs = animals_gifs
        self.gaming_gifs = gaming_gifs
        self.strange_gifs = strange_gifs
        self.educational_gifs = educational_gifs
        self.temp_count = temp_count

    def gif_counter(self, category):
        if category == 'all':
            self.all_gifs += 1
        elif category == 'animals':
            self.animals_gifs += 1
        elif category == 'gaming':
            self.gaming_gifs += 1
        elif category == 'strange':
            self.strange_gifs += 1
        elif category == 'educational':
            self.educational_gifs += 1
        self.temp_count += 1

    def readout(self):
        categories = ['all', 'animals', 'gaming', 'strange', 'educational']
        numbers = [self.all_gifs, self.animals_gifs, self.gaming_gifs, self.strange_gifs, self.educational_gifs]
        counter = 0
        print '\n'
        for entry in categories:
            print '%d GIFs added to %s_urls.txt' % (numbers[counter], entry)
            counter += 1


def scrape_reddit(target_subreddit, path, category):
    log.temp_count = 0
    clean_urls = []
    print '\nGathering image URLs from /r/%s...' % target_subreddit

    # Accessing Reddit API
    r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')
    submissions = r.get_subreddit(target_subreddit).get_hot(limit=200)

    # Creating Python list from url file
    with open('%s/%s_urls.txt' % (path, category), 'a+') as f:
        current_urls = list(f)

    for submission in submissions:
        if submission.url + '\n' in current_urls:
            continue
        elif not submission.url.endswith('.gif'):
            continue
        elif 'sound' in submission.url:
            continue
        else:
            try:
                request = requests.get(submission.url, stream=True)
                code = request.status_code
            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError):
                continue
            try:
                size = int(request.headers['content-length'])
                if size == 503:
                    continue
            except KeyError:
                clean_urls.append(submission.url + '\n')
                log.gif_counter(category)
            if code == 404:
                continue
            elif code == 302:
                continue
            else:
                clean_urls.append(submission.url + '\n')
                log.gif_counter(category)
    print '%d GIFs added from /r/%s' % (log.temp_count, target_subreddit)

    # Appending contents of clean_urls to current url file
    with open('%s/%s_urls.txt' % (path, category), 'a+') as f:
        for line in clean_urls:
            try:
                f.write(line)
            except UnicodeEncodeError:
                continue

if __name__ == '__main__':
    # Uncomment to run script off server
    # prompt = raw_input('Are you scraping from work or home? > ').lower()
    # if prompt == 'work':
    #     current_path = 'E:/programming/projects/blog/app/templates/pi_display/logs/'
    # else:
    #     current_path = 'H:/programming/projects/blog/app/templates/pi_display/logs/'

    # Server path
    current_path = '/home/tylerkershner/app/templates/pi_display/logs/'

    categories = ['all', 'animals', 'gaming', 'strange', 'educational']

    subreddits = [
        ['gifs', 'gif', 'blackpeoplegifs', 'SpaceGifs', 'physicsgifs', 'educationalgifs', 'chemicalreactiongifs',
         'SurrealGifs', 'Puggifs', 'slothgifs', 'asianpeoplegifs', 'gaming_gifs', 'Movie_GIFs', 'funnygifs',
         'wheredidthesodago', 'reactiongifs', 'creepy_gif', 'perfectloops', 'aww_gifs', 'AnimalsBeingJerks',
         'AnimalGIFs', 'whitepeoplegifs', 'interestinggifs', 'cinemagraphs', 'wtf_gifs',
         'MichaelBayGifs', 'naturegifs', 'pugs', 'gaming', 'Wastedgifs', 'GamePhysics', 'catgifs',
         'opticalillusions', 'wrestlinggifs', 'shittyreactiongifs', 'IdiotsFightingThings', 'Whatcouldgowrong',
         'interestingasfuck', 'AnimalsBeingBros', 'PerfectTiming', 'holdmybeer', 'StartledCats', 'combinedgifs',
         'Damnthatsinteresting', 'shittyrobots', 'catpranks', 'Awwwducational', 'instant_regret', 'oddlysatisfying',
         'Perfectfit', 'SuperShibe', 'shibe', 'corgi'],
        ['Puggifs', 'slothgifs', 'aww_gifs', 'AnimalsBeingJerks', 'AnimalGIFs', 'pugs', 'CatGifs', 'SuperShibe',
         'shibe', 'corgi', 'Awwducational', 'AnimalsBeingBros', 'StartledCats', 'catpranks'],
        ['gaming_gifs', 'gaming', 'GamePhysics', 'ps4gifs'],
        ['creepy_gif', 'wtf_gifs', 'SurrealGifs'],
        ['physicsgifs', 'educationalgifs', 'chemicalreactiongifs', 'interestinggifs', 'Damnthatsinteresting',
         'interestingasfuck']
    ]

    log = Log(0, 0, 0, 0, 0, 0)
    count = 0
    for entry in categories:
        print '\n####################################'
        print 'Now scraping %s subreddits' % entry
        print '####################################'
        for subreddit in subreddits[int('%d' % count)]:
            scrape_reddit(subreddit, current_path, entry)
        count += 1
    log.readout()