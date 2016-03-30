import requests
import praw
import time
from app import models, db


class Temp(object):
    def __init__(self, current_urls, bad_urls, to_add_urls):
        self.current_urls = current_urls
        self.bad_urls = bad_urls
        self.to_add_urls = to_add_urls


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
        print e
        return None
    # except (KeyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
    #     # No content-length HTTP header or error with request handshake
    #     return None


def get_reddit_urls(subreddit, tag_id):
    print '\nGathering image URLs from /r/%s...' % sub

    submissions = r.get_subreddit(subreddit.name).get_hot(limit=100)
    for submission in submissions:
        if submission.url.endswith('.gif'):
            temp.to_add_urls.append([tag_id, submission.url])


def process_urls(urls_list):
    print '\nProcessing URLs...'

    count = 1
    final_list = []
    for entry in urls_list:
        tag_id = entry[0]
        url = entry[1]
        try:
            if url not in temp.current_urls and url not in temp.bad_urls:
                url_data = request_url(url)
                if not url_data['code'] == 200:
                    print 'Status Code not 200.  Code: %d || %s' % (url_data['code'], url)
                elif url_data['float_size'] > 6.00:
                    print 'Gif too large.  Size: %f || %s' % (url_data['float_size'], url)
                else:
                    new_gif = models.Gif(url=url)
                    if tag_id is not None:
                        new_tag = models.Tag.query.get(tag_id)
                        new_gif.tags.append(new_tag)
                    db.session.add(new_gif)
                    final_list.append([tag_id, url])
                    print 'Adding GIF...(%d GIFs)' % count
                    count += 1
        except TypeError as e:
            print e
            continue

    print '\nCommitting DB session...'
    db.session.commit()
    print 'done!'

    print '\nTotal GIFs added: %d' % len(final_list)


if __name__ == '__main__':
    # Local path
    path = 'c:/programming/projects/blog/app/templates/pi_display/logs'

    # Server path
    # path = '/home/tylerkershner/app/templates/pi_display/logs/'

    with open('%s/%s' % (path, 'bad_urls.txt'), 'a+') as temp_file:
        bad_urls_list = [url.rstrip('\r\n') for url in temp_file]

    # Accessing Reddit API
    r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')

    temp = Temp(
        current_urls=[gif.url for gif in models.Gif.query.all()],
        bad_urls=bad_urls_list,
        to_add_urls=[]
    )

    start = time.time()

    subreddits = models.Subreddit.query.all()
    for sub in subreddits:
        get_reddit_urls(sub, sub.tag_id)

    process_urls(temp.to_add_urls)

    end = time.time()
    print '\nScript Execution Time: %.2f minutes' % (float(end - start) / 60.0)