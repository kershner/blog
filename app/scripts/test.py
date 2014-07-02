import requests
import time


# Function to determine size of URL via HTML header data
def getsize(url):
    try:
        r = requests.get(url, stream=True)
        size = int(r.headers['content-length'])
        return size
    except KeyError:
        return 'None'

# Opening files, converting to Python lists
urls_file = open('E:/programming/projects/blog/app/templates/pi_display/urls.txt', 'a+')
urls_list = list(urls_file)
bad_urls_file = open('E:/programming/projects/blog/app/templates/pi_display/bad_urls.txt', 'a+')
bad_urls_list = list(bad_urls_file)
large_urls_file = open('E:/programming/projects/blog/app/templates/pi_display/large_urls.txt', 'a+')
large_urls_list = list(large_urls_file)

# Variables to keep track of certain GIFs added
count = 0
bad_urls = 0
large_urls = 0

submissions = ['http://i.imgur.com/Pom1UDE.gif']

for url in submissions:
    # Wait 2 seconds, retry the URL if there is an error with the connection
    try:
        r = requests.get(url)
    except:
        try:
            time.sleep(2)
            r = requests.get(url)
        except:
            print 'Error requesting %s, skipping...' % url
            continue
    # Already in urls.txt
    if url + '\n' in urls_list:
        print '%s already in urls.txt...' % url
        continue
    # Known bad URL
    elif url + '\n' in bad_urls_list:
        print '%s in bad_urls.txt...' % url
        bad_urls += 1
        continue
    # Known Large URL
    elif url + '\n' in large_urls_list:
        print '%s in large_urls.txt' % url
        large_urls += 1
        continue
    # Not a .gif file
    if '.gif' not in url:
        print '%s is not a GIF file, skipping...' % url
        bad_urls_file.write(str(url) + '\n')
        bad_urls += 1
        continue
    # 404 status code is a broken link
    if r.status_code == 404:
        print '%s is a broken link (404), skipping...' % url
        # Logging bad URL
        bad_urls_file.write(str(url) + '\n')
        bad_urls += 1
        continue
    # 302 is redirection, meaning bad link
    if r.status_code == 302:
        print '%s is a broken link (302), skipping...' % url
        # Logging bad URL
        bad_urls_file.write(str(url) + '\n')
        bad_urls += 1
        continue
    # Don't want gifsound links
    if 'sound' in url:
        print '%s is a gifsound link, skipping...' % url
        bad_urls_file.write(str(url) + '\n')
        bad_urls += 1
        continue
    # If the getsize function returned None, there was an error
    if getsize(url) == 'None':
        print '%s has no length data in HTTP header, skipping...' % url
        bad_urls_file.write(str(url) + '\n')
        bad_urls += 1
        continue
    # The Pi has a hard time with GIFs larger than 8MBs
    elif getsize(url) > 8192000:
        print '%s is larger than 8MBs, skipping...' % url
        continue
    # Imgur 'removed' image is 503 bytes
    elif getsize(url) == 503:
        print '%s is a broken link (503 bytes), skipping...' % url
        urls_file.write(str(url) + '\n')
        bad_urls += 1
        continue
    else:
        print '%s not found in urls.txt, adding...' % url
        urls_file.write(str(url) + '\n')
        count += 1