import requests
from requests import exceptions
import socket

path = '/home/tylerkershner/app/templates/pi_display/logs'
diag_path = '/home/tylerkershner/app/templates/pi_display/logs/diagnostics'

with open('%s/all_urls.txt' % path, 'r') as urls_file:
        urls_list = list(urls_file)

no_content_length = []
too_large = []
good_urls = []
connection_error = []
gfycat = []
timeout = []

counter = 0
for url in urls_list:
    counter += 1
    url = url[:url.find('\n')]
    print 'URL %d of %d' % (counter, len(urls_list))
    if 'gfycat' in url:
        print '%s - gfycat URL, skipping...' % url
        gfycat.append(url)
    if 'instant_regret' in url:
        continue
    try:
        r = requests.get(url, timeout=3)
        size = float(r.headers['content-length']) / 1051038
        print '%s - %.2f Mb' % (url, size)
        if size > 6.00:
            print '%s is larger than 6 Mb, skipping...(%.2f)' % (url, size)
            too_large.append(url)
        else:
            # Acceptable URL
            good_urls.append(url)
    except KeyError:
        print '%s has no content-length in HTTP header, skipping...' % url
        no_content_length.append(url)
    except exceptions.ConnectionError:
        print 'Connection error with %s, skipping...' % url
        connection_error.append(url)
    except exceptions.Timeout:
        print '%s timed out, skipping...' % url
        timeout.append(url)
    except socket.timeout:
        print '%s URL timed out, skipping' % url
        timeout.append(url)

lists = [['no_content_length', no_content_length], ['too_large', too_large], 
        ['good_urls', good_urls], ['connetion_error', connection_error], 
        ['gfycat', gfycat], ['timeout', timeout]]

for list in lists:
    filename = '%s.txt' % list[0]
    with open('%s/%s' % (diag_path, filename), 'a+') as temp:
        for line in list[1]:
            temp.write(line + '\n')

print '\nURLs with no content-length header: %d' % len(no_content_length)
print 'URLs with connection errors: %d' % len(connection_error)
print 'URLs larger than 6 Mb: %d' % len(too_large)
print 'Gfycat URLs: %d' % len(gfycat)
print 'URLs timed out: %d' % len(timeout)
bad_urls = int(len(no_content_length) + len(connection_error) + len(too_large) + len(gfycat) + len(timeout))
print '\nTotal number of good URLs: %d' % int(len(good_urls) - bad_urls)