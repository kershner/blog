import praw
import requests
import urllib

file_object = open('E:/programming/projects/blog/app/templates/pi_display/test.txt', 'r')
file_object_list = list(file_object)


def getsize(uri):
    image_file = urllib.urlopen(uri)
    size = image_file.headers.get("content-length")
    if size is None:
        image_file.close()
        return 'None'
    else:
        image_file.close()
        return (int(size) / 1024) / 1024

count = 0

for url in file_object_list:
    if getsize(url) is 'None':
        count += 1

print '%d out of %d' % (count, len(file_object_list))


file_object.close()