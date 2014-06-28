import urllib


# Function to determine size of URL via HTML header data
def getsize(uri):
    image_file = urllib.urlopen(uri)
    size = image_file.headers.get("content-length")
    image_file.close()
    return int(size)

# Opening current URL file for reading
file_object = open('H:/programming/projects/blog/app/templates/pi_display/urls.txt', 'r')

# Converting text file to list object to more easily perform operations on it
urls = list(file_object)

count = 0
url_number = 0

imgur_404_urls = open('H:/programming/projects/blog/app/templates/pi_display/imgur_404_urls.txt', 'a')

for url in urls:
    # Removing newline character from URL
    end_point = url.find('\n')
    url = url[:end_point]
    url_number += 1
    print 'URL #%d of %d' % (url_number, len(urls))
    try:
        if getsize(url) == 503:
            print '%s is a broken link, skipping...' % url
            imgur_404_urls.write(str(url) + '\n')
            count += 1
    except TypeError:
        print 'No length data in HTTP header'


print '%d broken imgur links logged' % count


file_object.close()
imgur_404_urls.close()