# This script will comb though the current urls.txt generated by the reddit scraper and re-write it
# omitting broken links (and eventually images that are too large for the Pi
import urllib2
import time


# Function to determine size of URL via HTTP header data
def getsize(url):
    url = urllib2.urlopen(url)
    try:
        size = int(url.info()['content-length'])
        return size
    except:
        return 'None'

# Opening current URL file for reading
file_object = open('E:/programming/projects/blog/app/templates/pi_display/urls.txt', 'r')

# Creating list from urls.txt, closing the file
urls = list(file_object)
file_object.close()

# Opening (or creating) files to be used in the loop
clean_urls = open('E:/programming/projects/blog/app/templates/pi_display/clean_urls.txt', 'a+')
bad_urls = open('E:/programming/projects/blog/app/templates/pi_display/bad_urls.txt', 'a+')
bad_urls_list = list(bad_urls)
large_urls = open('E:/programming/projects/blog/app/templates/pi_display/large_urls.txt', 'a+')
large_urls_list = list(large_urls)

# Initializing variables to hold count of removed links, for logging
count = 0
url_number = 0
large_gifs = 0
duplicates = 0

# Loop to determine if link is broken/file too large.  URL written to either clean or bad URLs files.
for url in urls:
    url_number += 1
    print 'URL %d of %d' % (url_number, len(urls))
    try:
        r = urllib2.urlopen(url)
    except:
        print 'Error requesting %s' % url
        continue
    if url in bad_urls_list:
        print '%s is a known bad URL, skipping...' % url
        continue
    elif url in large_urls_list:
        print '%s is a known large URL, skipping...' % url
        continue
    # If the image 404s it's obviously a bad link
    if r.getcode() == 404:
        print '%s is a broken link (404), skipping...' % url
        # Logging bad URL
        bad_urls.write(str(url))
        count += 1
        continue
    # If the image 302s, we're being redirected (bad link)
    if r.getcode() == 302:
        print '%s is a broken link (302), skipping...' % url
        # Logging bad URL
        bad_urls.write(str(url))
        count += 1
        continue
    # The Pi has a hard time with GIFs larger than 8MBs
    if getsize(url) > 8192000:
        print '%s is larger than 8MBs, skipping...' % url
        large_gifs += 1
        large_urls.write(str(url))
        continue
    # Imgur 'removed' image is 503 bytes
    elif getsize(url) == 503:
        print '%s is a broken link (503 bytes), skipping...' % url
        bad_urls.write(str(url))
        count += 1
        continue
    elif getsize(url) == 'None':
        print '%s has no length data in HTTP header, skipping...' % url
        count += 1
        continue
    else:
        print 'Clean URL, adding...'
        clean_urls.write(str(url))

# Closing files
clean_urls.close()
bad_urls.close()
large_urls.close()

# Creating Python list from newly populated clean_urls.txt
updated_clean_urls = open('E:/programming/projects/blog/app/templates/pi_display/clean_urls.txt', 'r')
clean_urls_list = list(updated_clean_urls)
updated_clean_urls.close()

# Opening/closing urls.txt (taking advantage of side effect to erase contents)
open('E:/programming/projects/blog/app/templates/pi_display/urls.txt', 'w').close()

# Re-opening urls.txt, appending with contents of the clean_urls.txt list, closing the file
url_file = open('E:/programming/projects/blog/app/templates/pi_display/urls.txt', 'a+')
for url in clean_urls_list:
    url_file.write(url)
url_file.close()

# Opening updated file, printing # of URLs
with open('E:/programming/projects/blog/app/templates/pi_display/urls.txt', 'r') as f:
    number_of_gifs = len(list(f))
    print '\nNumber of GIFS: %d' % number_of_gifs
print '%d bad links removed' % count
print '%d duplicates removed' % duplicates
print '%d large GIFs removed' % large_gifs

# Opening and closing the clean_urls.txt file.  Side effect to erase contents of file.
print '\n\n\n\nErasing contents of clean_urls.txt...'
open('E:/programming/projects/blog/app/templates/pi_display/clean_urls.txt', 'w').close()