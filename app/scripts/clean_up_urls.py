from time import time
import concurrent.futures
import requests
from tqdm import tqdm
from time import sleep
from app import db, models


class Log(object):
    def __init__(self, gif_list, removed_urls, exceptions):
        self.gif_list = gif_list
        self.removed_urls = removed_urls
        self.exceptions = exceptions


def remove_dupes(gif_list):
    print '\n\n######################'
    print 'Beginning Dupe Removal'

    dupes = []
    progress_bar = tqdm(gif_list)
    for gif in progress_bar:
        if gif.url in dupes:
            print '\n\n%s is a duplicate gif, removing...\n\n' % gif.url
            log.removed_urls.append(gif.url)
        else:
            dupes.append(gif.url)


def clean_up_urls(gif_list):
    print '\n######################'
    print 'Beginning GIF cleanup'

    progress_bar = tqdm(gif_list)
    for gif in progress_bar:
        if gif.url in bad_urls_list:
            print '%s is in the bad_urls_list, removing...' % gif.url
            log.removed_urls.append(gif.url)
        elif not gif.url.endswith('.gif'):
            print '%s is not a .gif file, removing...' % gif.url
            log.removed_urls.append(gif.url)

    send_requests(gif_list)


def send_requests(gif_list):
    print '\n######################'
    print 'Sending Requests'

    gif_list = [gif.url for gif in gif_list]
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        pages = executor.map(load_url, gif_list)


def load_url(gif_url):
    log.gif_list.remove(gif_url)

    try:
        r = requests.get(gif_url, stream=True, timeout=1)
        code = r.status_code
        if not code == 200:
            print '%d | %d GIFs remaining | %s' % (code, len(log.gif_list), gif_url)
            log.removed_urls.append(gif_url)
        else:
            print '%d | %d GIFs remaining | %s' % (code, len(log.gif_list), gif_url)
    except Exception as e:
        print '\n\n@@@@@@@@@@@@@@@@@@'
        print 'ERROR - ', e.message
        log.exceptions.append(gif_url)
        print '@@@@@@@@@@@@@@@@@@\n\n'


def final_pass(gif_list):
    print '\n######################'
    print 'Final Pass'

    sleep(5)

    for gif in gif_list:
        if gif.url in log.removed_urls:
            db.session.delete(gif)

    print '\nCommitting session...'
    db.session.commit()
    print 'done!'


if __name__ == '__main__':
    # Local path
    path = 'c:/programming/projects/blog/app/templates/pi_display/logs'

    # Server path
    # path = '/home/tylerkershner/app/templates/pi_display/logs/'

    gifs = models.Gif.query.all()
    with open('%s/%s' % (path, 'bad_urls.txt'), 'a+') as temp_file:
        bad_urls_list = [url.rstrip('\r\n') for url in temp_file]

    gif_list_copy = [gif.url for gif in gifs]
    log = Log(gif_list_copy, [], [])

    start = time()
    remove_dupes(gifs)
    clean_up_urls(gifs)
    final_pass(gifs)
    end = time()

    print '## READOUT ##############################'
    print '\n%d GIFs removed' % len(log.removed_urls)
    print log.removed_urls
    print '\nCurrent Gif Total: %d' % len(models.Gif.query.all())

    print '\nScript Execution Time: %.2f minutes' % (float(end - start) / 60.0)

    print '\n%d Exceptions:' % len(log.exceptions)
    print log.exceptions
