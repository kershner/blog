import requests

#file_object = open('/home/tylerkershner/app/templates/pi_display/urls.txt', 'r+')
file_object = open('e:/programming/projects/blog/app/templates/pi_display/urls.txt', 'r+')
clean_urls = 'e:/programming/projects/blog/app/templates/pi_display/clean_urls.txt'
bad_urls = 'e:/programming/projects/blog/app/templates/pi_display/bad_urls.txt'

urls = list(file_object)

count = 0

for url in urls:
    end_point = url.find('\n')
    url = url[:end_point]
    try:
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 302:
            print '%s is a broken link, skipping...' % url
            with open(bad_urls, 'w') as f:
                f.write(url)
                f.write('\n')
            count += 1
        else:
            print 'Clean url, adding...'
            with open(clean_urls, 'w') as f:
                f.write(url)
                f.write('\n')
    except requests.ConnectionError:
        print 'Connection failed, skipping...'
        pass


print '%d links removed' % count

file_object.close()