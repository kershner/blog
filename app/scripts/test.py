import requests

# Function to determine size of URL via HTML header data
def getsize(url):
    try:
        r = requests.get(url, stream=True)
        size = r.headers['content-length']
        return int(size)
    except KeyError:
        return 'None'

this_url = 'http://i.minus.com/ibhtxs1tWpNcqY.gif'
if getsize(this_url) == 'None':
    print 'Error in this shit'
else:
    print 'Gif is larger than 8MBs'
    print getsize(this_url)
