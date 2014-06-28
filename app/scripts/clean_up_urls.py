# This script will comb though the current urls.txt generated by the reddit scraper and re-write it
# omitting broken links (and eventually images that are too large for the Pi
import urllib


# Function to determine size of URL via HTML header data
def getsize(uri):
    image_file = urllib.urlopen(uri)
    size = image_file.headers.get("content-length")
    image_file.close()
    return int(size)

# Opening current URL file for reading
file_object = open('H:/programming/projects/blog/app/templates/pi_display/urls.txt', 'r')

# Creating list from urls.txt, closing the file
urls = list(file_object)
file_object.close()

# Opening (or creating) files to be used in the loop
clean_urls = open('H:/programming/projects/blog/app/templates/pi_display/clean_urls.txt', 'a+')
bad_urls = open('H:/programming/projects/blog/app/templates/pi_display/bad_urls.txt', 'a')
large_urls = open('H:/programming/projects/blog/app/templates/pi_display/large_urls.txt', 'a')

# Initializing variables to hold count of removed links, for logging
count = 0
large_gifs = 0

# Loop to determine if link is broken/file too large.  URL written to either clean or bad URLs files.
for url in urls:
    # Removing newline character from URL
    end_point = url.find('\n')
    url = url[:end_point]
    print url
    r = urllib.urlopen(url)
    try:
        # Imgur 'removed' image is 503 bytes
        if getsize(url) == 503:
            print '%s is a broken link, skipping...' % url
            bad_urls.write(str(url) + '\n')
            count += 1
        # If the image 404s, it's obviously a bad link
        elif r.getcode() == 404:
            print '%s is a broken link, skipping...' % url
            # Logging bad URL
            with open('H:/programming/projects/blog/app/templates/pi_display/404_urls.txt', 'a') as f:
                f.write(url + '\n')
        # If the image 302s, we're being redirected (bad link)
        elif r.getcode() == 302:
            print '%s is a broken link, skipping...' % url
            # Logging bad URL
            with open('H:/programming/projects/blog/app/templates/pi_display/304_urls.txt', 'a') as e:
                e.write(url + '\n')
        # The Pi has a hard time with GIFs larger than 8MBs
        elif getsize(url) > 8192000:
            print '%s is larger than 8MBs, skipping...' % url
            large_gifs += 1
            large_urls.write(str(url) + '\n')
        else:
            print 'Clean URL, adding...'
            clean_urls.write(str(url) + '\n')
    except (TypeError, IOError):
        try:
            print '%s has No length data in HTML header or connection error, adding...' % url
            clean_urls.write(str(url) + '\n')
        except:
            pass

# Closing files
clean_urls.close()
bad_urls.close()
large_urls.close()

# Creating Python list from newly populated clean_urls.txt
updated_clean_urls = open('H:/programming/projects/blog/app/templates/pi_display/clean_urls.txt', 'r')
clean_urls_list = list(updated_clean_urls)
updated_clean_urls.close()

# Opening/closing urls.txt (taking advantage of side effect to erase contents)
open('H:/programming/projects/blog/app/templates/pi_display/urls.txt', 'w').close()

# Re-opening urls.txt, appending with contents of the clean_urls.txt list, closing the file
url_file = open('H:/programming/projects/blog/app/templates/pi_display/urls.txt', 'a+')
for url in clean_urls_list:
    url_file.write(url)
url_file.close()

# Opening updated file, printing # of URLs
with open('H:/programming/projects/blog/app/templates/pi_display/urls.txt', 'r') as f:
    number_of_gifs = len(list(f))
    print '\nNumber of GIFS: %d' % number_of_gifs
print '%d bad links removed' % count
print '%d large GIFs removed' % large_gifs

# Opening and closing the clean_urls.txt file.  Side effect to erase contents of file.
print '\n\n\n\nErasing contents of clean_urls.txt...'
open('H:/programming/projects/blog/app/templates/pi_display/clean_urls.txt', 'w').close()