import random
import re
import praw


# Simple code to match substring
def find_string(sub_string):
    return re.compile(r'\b({0})\b'.format(sub_string), flags=re.IGNORECASE).search


# Returns list of suggestions for subreddits
def picks():
    suggestions = ['pugs', 'earthporn', 'kittens', 'gaming', 'pics', 'awww', 'funny', 'adviceanimals', 'gifs',
                   'wallpapers', 'foodporn', 'historyporn', 'photoshopbattles', 'mildlyinteresting', 'woahdude',
                   'oldschoolcool', 'perfecttiming', 'abandonedporn', 'roomporn']
    p = []
    for number in range(0, 3):
        pick = random.choice(suggestions)
        if pick in p:
            continue
        else:
            p.append(pick)
    return p


# Main API scraper
def scrape_reddit(subreddit, results_from, number, min_score):
    good_urls = []
    indirect_urls = []

    r = praw.Reddit(user_agent='reddit scraper by billcrystals')

    try:
        test = r.get_subreddit(subreddit).id
    except praw.errors.InvalidSubreddit as e:
        return 'no subreddit'

    if results_from == 1:
        submissions = r.get_subreddit(subreddit).get_hot(limit=number)
        results_from = 'Hot'
    elif results_from == 2:
        submissions = r.get_subreddit(subreddit).get_top_from_all(limit=number)
        results_from = 'All'
    elif results_from == 3:
        submissions = r.get_subreddit(subreddit).get_top_from_year(limit=number)
        results_from = 'Year'
    else:
        submissions = r.get_subreddit(subreddit).get_top_from_month(limit=number)
        results_from = 'Month'

    for submission in submissions:
        if submission.score < min_score:
            continue
        elif submission.url.startswith('imgur.com/'):
            endpoint = submission.url.find('.com/')
            url = 'i.' + submission.url[:endpoint] + '.jpg'
            good_urls.append([url, submission.short_link, submission.title])
        elif find_string('/r/')(submission.url):
            if find_string('imgur')(submission.url):
                endpoint = submission.url.rfind('/')
                url = 'http://i.imgur.com' + submission.url[endpoint:] + '.jpg'
                good_urls.append([url, submission.short_link, submission.title])
            else:
                indirect_urls.append([submission.url, submission.short_link, submission.title])
        elif find_string('/gallery/')(submission.url):
            indirect_urls.append([submission.url, submission.short_link, submission.title])
        elif find_string('http://imgur.com/')(submission.url):
            if find_string('/a/')(submission.url):
                indirect_urls.append([submission.url, submission.short_link, submission.title])
            else:
                endpoint = submission.url.find('.com/')
                url = submission.url[endpoint + 5:]
                new_url = 'http://i.imgur.com/%s.jpg' % url
                if len(submission.title) > 75:
                    try:
                        submission.title = str(submission.title[:75]) + '...'
                        good_urls.append([new_url, submission.short_link, submission.title])
                    except UnicodeError:
                        continue
                else:
                    good_urls.append([new_url, submission.short_link, submission.title])
        elif find_string('qkme')(submission.url):
            indirect_urls.append([submission.url, submission.short_link, submission.title])
        elif find_string('youtube')(submission.url):
            indirect_urls.append([submission.url, submission.short_link, submission.title])
        elif find_string('twitter')(submission.url):
            indirect_urls.append([submission.url, submission.short_link, submission.title])
        elif '?' in submission.url:
            endpoint = submission.url.find('?')
            url = submission.url[:endpoint]
            if len(submission.title) > 75:
                try:
                    submission.title = str(submission.title[:75]) + '...'
                    good_urls.append([url, submission.short_link, submission.title])
                except UnicodeError:
                    continue
            else:
                good_urls.append([url, submission.short_link, submission.title])
        elif not submission.url.endswith(('.gif', '.png', '.jpg', '.jpeg')):
            indirect_urls.append([submission.url, submission.short_link, submission.title])
        else:
            if len(submission.title) > 75:
                try:
                    submission.title = str(submission.title[:75]) + '...'
                    good_urls.append([submission.url, submission.short_link, submission.title])
                except UnicodeError:
                    continue
            else:
                good_urls.append([submission.url, submission.short_link, submission.title])

    data = {
        'good_urls': good_urls,
        'indirect_urls': indirect_urls,
        'good_urls_number': len(good_urls),
        'indirect_urls_number': len(indirect_urls),
        'results_from': results_from
    }

    return data
