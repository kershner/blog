#import urllib
import requests

try:
    r = requests.get('http://www.picsarus.com/53FBHN.gif', timeout=1)
except requests.exceptions.Timeout:
    print 'Error occured!'

print r.status_code()