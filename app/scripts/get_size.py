import urllib

file_object = open('e:/programming/projects/blog/app/templates/pi_display/urls.txt', 'r+')
urls = list(file_object)
total = 0

def getsize(uri):
    file = urllib.urlopen(uri)
    size = file.headers.get("content-length")
    file.close()
    return int(size) / 1024

for url in urls:
    try:
        total += getsize(url)
        print "%s\t\t\tSize: %d KB" % (url, getsize(url))
    except (TypeError, IOError):
        print 'No content-length in header, skipping...'
        pass