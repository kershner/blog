from time import time
import concurrent.futures
import requests
from tqdm import tqdm
from time import sleep
from app import db, models


class Log(object):
    def __init__(self, gif_list, removed_gifs, banned_strings, exceptions):
        self.gif_list = gif_list
        self.removed_gifs = removed_gifs
        self.banned_strings = banned_strings
        self.exceptions = exceptions


def clean_up_urls(gif_list):
    dupes_test = []
    for gif in gif_list:
        logged_gif = {
            'url': gif.url
        }
        if gif.url in dupes_test:
            logged_gif['reason'] = 'dupe'
            log.removed_gifs.append(logged_gif)
        elif gif.url in bad_urls_list:
            logged_gif['reason'] = 'In bad URLs list'
            log.removed_gifs.append(logged_gif)
        elif not gif.url.endswith('.gif'):
            logged_gif['reason'] = 'Not a .gif'
            log.removed_gifs.append(logged_gif)
        else:
            for string in log.banned_strings:
                if string in gif.url:
                    logged_gif['reason'] = '%s in URL' % string
                    log.removed_gifs.append(logged_gif)

        dupes_test.append(gif.url)

    send_requests(gif_list)


def send_requests(gif_list):
    gif_list = [gif.url for gif in gif_list]

    # Traditional
    # for url in gif_list:
    #     load_url(url)

    # Threaded Black Magic
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        pages = executor.map(load_url, gif_list)


def load_url(gif_url):
    log.gif_list.remove(gif_url)
    logged_gif = {
        'url': gif_url
    }

    try:
        r = requests.get(gif_url, stream=True, timeout=5, allow_redirects=True)
        code = r.status_code
        size_in_bytes = int(r.headers['content-length'])
        float_size = float(size_in_bytes) / 1051038
        # print '%d | %d GIFs remaining | %s' % (code, len(log.gif_list), gif_url)
        if not code == 200:
            logged_gif['code'] = code
            logged_gif['reason'] = 'Code not 200'
            log.removed_gifs.append(logged_gif)
        if float_size == 503:
            logged_gif['reason'] = 'Size is 503'
            log.removed_gifs.append(logged_gif)

    except Exception as e:
        logged_gif['reason'] = e.args[0]
        log.exceptions.append(logged_gif)


def final_pass(gif_list):
    sleep(5)

    removed_urls = [removed_gif['url'] for removed_gif in log.removed_gifs]
    for gif in gif_list:
        if gif.url in removed_urls:
            db.session.delete(gif)

    db.session.commit()


if __name__ == '__main__':
    gifs = models.Gif.query.all()
    bad_urls_list = [url.url for url in models.BadUrl.query.all()]

    gif_list_copy = [gif.url for gif in gifs]
    log = Log(gif_list_copy, [], [], [])
    log.banned_strings = ['gifsec', 'redditmetrics', 'thecooltshirt', '5secondsapp', 'gifsoup']

    start = time()
    clean_up_urls(gifs)
    final_pass(gifs)
    end = time()

    print '## clean_up_urls Readout ###############################################################'
    print '\n%d GIFs removed' % len(log.removed_gifs)
    print log.removed_gifs
    print '\n%d Exceptions' % len(log.exceptions)
    print log.exceptions
    print '\nCurrent Gif Total: %d' % len(models.Gif.query.all())
    print '\nScript Execution Time: %.2f minutes' % (float(end - start) / 60.0)