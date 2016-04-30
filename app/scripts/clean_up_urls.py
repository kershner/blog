from time import time
import concurrent.futures
from tqdm import tqdm
from cStringIO import StringIO
from PIL import Image
from time import sleep
from app import db, models
import requests
import os
import pprint


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
        r = requests.get(gif_url, stream=True, timeout=5, allow_redirects=False)
        code = r.status_code
        # print '%d | %d GIFs remaining | %s' % (code, len(log.gif_list), gif_url)
        if not code == 200:
            logged_gif['code'] = code
            logged_gif['reason'] = 'Code not 200'
            log.removed_gifs.append(logged_gif)

    except Exception as e:
        logged_gif['reason'] = e.args[0]
        log.exceptions.append(logged_gif)
        log.removed_gifs.append(logged_gif)


def final_pass(gif_list):
    sleep(5)

    removed_urls = [removed_gif['url'] for removed_gif in log.removed_gifs]
    for gif in gif_list:
        if gif.url in removed_urls:
            db.session.delete(gif)
            # Remove thumbnail
            try:
                base_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
                filename = base_path + '/static/pi_display/thumbnails/%d.jpeg' % gif.id
                # print 'Deleting thumbnail: %s' % filename
                os.remove(filename)
            except Exception as e:
                # print e
                pass
        else:
            create_thumbnail(gif)

    db.session.commit()


def create_thumbnail(gif):
    base_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    filename = base_path + '/static/pi_display/thumbnails/%d.jpeg' % gif.id
    if not (os.path.isfile(filename)):
        # print 'Attempting to save thumbnail for Gif %d...' % gif.id
        size = (150, 150)
        img = requests.get(gif.url)
        img = StringIO(img.content)
        try:
            img_file = Image.open(img).convert('RGB').resize(size)
            img_file.thumbnail(size, Image.ANTIALIAS)
            img_file.save(filename, 'JPEG')
        except IOError as e:
            # print 'Gif %d - ' % gif.id, e
            pass

if __name__ == '__main__':
    gifs = models.Gif.query.all()
    bad_urls_list = [url.url for url in models.BadUrl.query.all()]

    gif_list_copy = [gif.url for gif in gifs]
    log = Log(gif_list_copy, [], [], [])
    log.banned_strings = ['gifsec', 'redditmetrics', 'thecooltshirt', '5secondsapp', 'gifsoup', '#/media/File:']

    start = time()
    clean_up_urls(gifs)
    final_pass(gifs)
    end = time()

    print '## clean_up_urls Readout ###############################################################'
    print '\n%d GIFs removed' % len(log.removed_gifs)
    print '\n%d Exceptions' % len(log.exceptions)
    print '\nCurrent Gif Total: %d' % len(models.Gif.query.all())
    print '\nScript Execution Time: %.2f minutes' % (float(end - start) / 60.0)
    pprint(log.removed_gifs)