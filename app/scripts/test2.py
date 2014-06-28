import urllib

# Function to determine size of URL via HTML header data
def getsize(uri):
    image_file = urllib.urlopen(uri)
    size = image_file.headers.get("content-length")
    image_file.close()
    return int(size)

url = 'http://i.imgur.com/0utpx.gif'

print getsize(url)
