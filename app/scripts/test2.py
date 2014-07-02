import requests
import time

test_urls_file = open('E:/programming/projects/blog/app/templates/pi_display/test.txt', 'r')
test_urls_list = list(test_urls_file)

# Function to determine size of URL via HTML header data
def getsize(url):
    try:
        r = requests.get(url, stream=True)
    except:
        try:
            time.sleep(2)
            r = requests.get(url, stream=True)
        except:
            print 'Error requesting %s, skipping...' % url
            return 'Connection Error'
    try:
        size = int(r.headers['content-length'])
        return size / 1024.0
    except KeyError:
        return 'None'

for url in test_urls_list:
    if getsize(url) is 'None':
        print '%s - no length data...' % url
        continue
    elif getsize(url) is 'Connection Error':
        print 'Error connecting to %s, skipping...' % url
        continue
    else:
        print '%s - %d KBs' % (url, getsize(url))


test_urls_file.close()