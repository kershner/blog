import requests
import praw
import time
from datetime import datetime
from app import models, db

requests.packages.urllib3.disable_warnings()


class Temp(object):
    def __init__(self, current_urls, bad_urls, to_add_urls, final_list, processed_subs, submission_limit):
        self.current_urls = current_urls
        self.bad_urls = bad_urls
        self.to_add_urls = to_add_urls
        self.final_list = final_list
        self.processed_subs = processed_subs
        self.submission_limit = submission_limit


def request_url(url):
    try:
        r = requests.get(url, stream=True, timeout=1, allow_redirects=False)
        size_in_bytes = int(r.headers['content-length'])
        float_size = float(size_in_bytes) / 1051038
        code = r.status_code
        data = {
            'size': size_in_bytes,
            'float_size': float_size,
            'code': code
        }
        return data
    except Exception as e:
        # print e
        return None


def get_reddit_urls(subreddit, limit):
    # print '\nGrabbing submissions from /r/%s...' % subreddit.name
    submissions = r.get_subreddit(subreddit.name).get_hot(limit=limit)

    # print 'About to process %d submissions...' % len(list(submissions))
    gifcount = 0
    for submission in submissions:
        if submission.url.endswith('.gif'):
            gifcount += 1
            temp.to_add_urls.append([subreddit.tags, submission.url])

    # print '%d GIFs added from r/%s' % (gifcount, subreddit.name)


def process_urls(urls_list):

    urlcount = 0
    final_list = []
    for entry in urls_list:
        urlcount += 1
        tags = entry[0]
        url = entry[1]
        # print 'Processing URL %d of %d...' % (urlcount, len(urls_list))
        try:
            if url not in temp.current_urls and url not in temp.bad_urls:
                url_data = request_url(url)
                if not url_data['code'] == 200:
                    continue
                elif url_data['float_size'] > 6.00:
                    continue
                else:
                    new_gif = models.Gif(url=url, created_at=datetime.now())
                    for tag in tags:
                        new_gif.tags.append(tag)
                    db.session.add(new_gif)
                    final_list.append([tags, url])
        except TypeError as e:
            # print e
            continue

    temp.final_list = final_list
    db.session.commit()


if __name__ == '__main__':
    # Accessing Reddit API
    r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')

    temp = Temp(
        current_urls=[gif.url for gif in models.Gif.query.all()],
        bad_urls=[url.url for url in models.BadUrl.query.all()],
        to_add_urls=[],
        final_list=[],
        processed_subs=1,
        submission_limit=150
    )

    start = time.time()
    subreddits = models.Subreddit.query.all()

    for sub in subreddits:
        get_reddit_urls(sub, temp.submission_limit)
        temp.processed_subs += 1

    process_urls(temp.to_add_urls)
    end = time.time()

    print '\n\n## scrape_reddit Readout ###############################################################'
    print '%d GIFs added' % len(temp.final_list)
    print 'Script Execution Time: %.2f minutes\n\n\n\n' % (float(end - start) / 60.0)
    # print temp.final_list
