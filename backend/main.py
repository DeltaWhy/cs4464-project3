import httplib2 as http
import urllib
import json
import feedparser

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}

def extractEntities(url):
    uri = 'http://access.alchemyapi.com'
    path = '/calls/url/URLGetRankedNamedEntities'
    query = '?' + urllib.parse.urlencode({
        'url': url,
        'apikey': '1bfa1ea9bb37171aa55db5eedcf90eb1d719c6bb',
        'outputMode': 'json'
    })

    target = urlparse(uri+path+query)
    method = 'GET'
    body = ''

    h = http.Http()

    response, content = h.request(
            target.geturl(),
            method,
            body,
            headers)
    content = content.decode('utf-8')

    return json.loads(content)['entities']

def extractKeywords(url):
    uri = 'http://access.alchemyapi.com'
    path = '/calls/url/URLGetRankedKeywords'
    query = '?' + urllib.parse.urlencode({
        'url': url,
        'apikey': '1bfa1ea9bb37171aa55db5eedcf90eb1d719c6bb',
        'outputMode': 'json'
    })

    target = urlparse(uri+path+query)
    method = 'GET'
    body = ''

    h = http.Http()

    response, content = h.request(
            target.geturl(),
            method,
            body,
            headers)
    content = content.decode('utf-8')

    return json.loads(content)['keywords']

#print(extractKeywords('http://edition.cnn.com/2013/06/26/world/meast/israel-settlement-kerry/index.html'))
print(json.dumps(feedparser.parse('http://rss.cnn.com/rss/edition.rss')['entries']))
