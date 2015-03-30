import random
import re
import praw
import requests
from flask import render_template
from app import forms


def find_string(sub_string):
    return re.compile(r'\b({0})\b'.format(sub_string), flags=re.IGNORECASE).search


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


def scrape_reddit(subreddit, results_from, number, min_score):
    good_urls = []
    indirect_urls = []

    r = praw.Reddit(user_agent='reddit scraper by billcrystals')

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

    try:
        for submission in submissions:
            if submission.score < min_score:
                print 'Submission (%s) lower than requested min score.' % submission.url
                continue
            elif submission.url.startswith('imgur.com/'):
                endpoint = submission.url.find('.com/')
                url = 'i.' + submission.url[:endpoint] + '.jpg'
                good_urls.append([url, submission.short_link, submission.title])
            elif find_string('/r/')(submission.url):
                if find_string('imgur')(submission.url):
                    print '/r/ found in %s' % submission.url
                    endpoint = submission.url.rfind('/')
                    url = 'http://i.imgur.com' + submission.url[endpoint:] + '.jpg'
                    good_urls.append([url, submission.short_link, submission.title])
                else:
                    indirect_urls.append([submission.url, submission.short_link, submission.title])
            elif find_string('/gallery/')(submission.url):
                print 'Submission (%s) is an Imgur album link' % submission.url
                indirect_urls.append([submission.url, submission.short_link, submission.title])
            elif find_string('http://imgur.com/')(submission.url):
                if find_string('/a/')(submission.url):
                    print 'Submission (%s) is an Imgur album link' % submission.url
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
                print 'QKME link, adding to indirect_urls...'
                indirect_urls.append([submission.url, submission.short_link, submission.title])
            elif find_string('youtube')(submission.url):
                print 'Youtube link, adding to indirect_urls...'
                indirect_urls.append([submission.url, submission.short_link, submission.title])
            elif find_string('twitter')(submission.url):
                print 'Twitter link, adding to indirect_urls...'
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
                print 'Indirect URL: %s' % submission.url
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
    except (praw.errors.RedirectException, requests.HTTPError):
        return 'no subreddit'

    data = {
        'good_urls': good_urls,
        'indirect_urls': indirect_urls,
        'good_urls_number': len(good_urls),
        'indirect_urls_number': len(indirect_urls),
        'results_from': results_from
    }

    return data