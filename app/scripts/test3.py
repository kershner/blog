import requests

url = 'http://i.imgur.com/Pom1UDE.gif'

# Function to determine size of URL via HTML header data
def getsize(url):
    try:
        r = requests.get(url, stream=True)
        size = int(r.headers['content-length'])
        return size
    except KeyError:
        return 'None'


print getsize(url) > 8192000