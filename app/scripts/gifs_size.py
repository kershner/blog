import urllib2

path = 'h:'

size = 0
url_number = 0


def getsize(url):
        url = urllib2.urlopen(url)
        try:
            size = int(url.info()['content-length'])
            return size
        except KeyError:
            print '%s has no content-length data in HTTP header, skipping...' % url
            return 'None'

urls_file = open('%s/programming/projects/blog/app/templates/pi_display/urls.txt' % path, 'r')
urls_list = list(urls_file)

for url in urls_list:
    url_number += 1
    print 'Processing %d of %d' % (url_number, len(urls_list))
    try:
        r = urllib2.urlopen(url)
        try:
            size += getsize(url)
        except TypeError:
            print 'TypeError: skipping URL...'
            continue
    except (urllib2.HTTPError, urllib2.URLError):
        print '%s returns 403 forbidden or timed out, skipping...' % url
        continue

print '\n\n\nTotal size of %d GIFs:' % len(urls_list)
print '%d bytes' % size
print '%d KB' % (size / 1024)
print '%d MB' % ((size / 1024) / 1024)
print '%d GB' % (((size / 1024) / 1024) / 1024)
