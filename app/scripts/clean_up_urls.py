from time import time
import concurrent.futures
import requests
from tqdm import tqdm
from time import sleep
from app import db, models


class Log(object):
    def __init__(self, gif_list, removed_gifs):
        self.gif_list = gif_list
        self.removed_gifs = removed_gifs


def remove_dupes(gif_list):
    print '\n\n######################'
    print 'Beginning Dupe Removal'

    dupes = []
    progress_bar = tqdm(gif_list)
    for gif in progress_bar:
        if gif.url in dupes:
            print '\n\n%s is a duplicate gif, removing...\n\n' % gif.url
            logged_gif = {
                'url': gif.url,
                'reason': 'Dupe'
            }
            log.removed_gifs.append(logged_gif)
        else:
            dupes.append(gif.url)


def clean_up_urls(gif_list):
    print '\n######################'
    print 'Beginning GIF cleanup'

    gifs = tqdm(gif_list)
    for gif in gifs:
        if gif.url in bad_urls_list:
            print '%s is in the bad_urls_list, removing...' % gif.url
            logged_gif = {
                'url': gif.url,
                'reason': 'In bad URLs list'
            }
            log.removed_gifs.append(logged_gif)
        elif not gif.url.endswith('.gif'):
            logged_gif = {
                'url': gif.url,
                'reason': 'Not a .gif'
            }
            print '%s is not a .gif file, removing...' % gif.url
            log.removed_gifs.append(logged_gif)

    send_requests(gif_list)


def send_requests(gif_list):
    print '\n######################'
    print 'Sending Requests'

    gif_list = [gif.url for gif in gif_list]

    # Traditional
    # for url in gif_list:
    #     load_url(url)

    # Threaded Black magic
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        pages = executor.map(load_url, gif_list)


def load_url(gif_url):
    log.gif_list.remove(gif_url)

    try:
        r = requests.get(gif_url, stream=True, timeout=5)
        code = r.status_code
        if not code == 200:
            print '%d | %d GIFs remaining | %s' % (code, len(log.gif_list), gif_url)
            logged_gif = {
                'url': gif.url,
                'code': code,
                'reason': 'Code not 200'
            }
            log.removed_gifs.append(logged_gif)
        else:
            print '%d | %d GIFs remaining | %s' % (code, len(log.gif_list), gif_url)
    except Exception as e:
        print '\n\n@@@@@@@@@@@@@@@@@@'
        print 'ERROR - %s | %s' % (e.message, gif_url)
        # logged_gif = {
        #     'url': gif.url,
        #     'reason': e.message
        # }
        # log.removed_gifs.append(logged_gif)
        print '@@@@@@@@@@@@@@@@@@\n\n'


def final_pass(gif_list):
    print '\n######################'
    print 'Final Pass'

    sleep(5)

    removed_urls = [removed_gif['url'] for removed_gif in log.removed_gifs]
    for gif in gif_list:
        if gif.url in removed_urls:
            db.session.delete(gif)

    print '\nCommitting session...'
    db.session.commit()
    print 'done!'


if __name__ == '__main__':
    gifs = models.Gif.query.all()
    bad_urls_list = [url.url for url in models.BadUrl.query.all()]

    gif_list_copy = [gif.url for gif in gifs]
    log = Log(gif_list_copy, [])

    start = time()
    remove_dupes(gifs)
    clean_up_urls(gifs)
    final_pass(gifs)
    end = time()

    print '## READOUT ##############################'
    print '\n%d GIFs removed' % len(log.removed_gifs)
    print log.removed_gifs
    print '\nCurrent Gif Total: %d' % len(models.Gif.query.all())

    print '\nScript Execution Time: %.2f minutes' % (float(end - start) / 60.0)

    input('\n\nPress any key to exit...')