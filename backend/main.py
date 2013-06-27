import httplib2 as http
import json

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}

uri = 'http://access.alchemyapi.com'
path = '/calls/url/URLGetRankedNamedEntities?url=http://edition.cnn.com/2013/06/26/world/meast/israel-settlement-kerry/index.html&apikey=1bfa1ea9bb37171aa55db5eedcf90eb1d719c6bb&outputMode=json'

target = urlparse(uri+path)
method = 'GET'
body = ''

h = http.Http()

response, content = h.request(
        target.geturl(),
        method,
        body,
        headers)
content = content.decode('utf-8')

data = json.loads(content)['entities']

print(data)
