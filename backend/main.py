#!/usr/bin/python3

import httplib2 as http
import urllib
import json
import feedparser
import sys
import os

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}

def notify(msg):
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()

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

def citiesFromEntities(entities):
    cities = []
    for e in entities:
        if e['type'] != 'City':
            continue
        if ('disambiguated' in e) and ('name' in e['disambiguated']):
            cities.append(e['disambiguated']['name'])
        else:
            cities.append(e['text'])
    return cities

def countriesFromEntities(entities):
    countries = []
    for e in entities:
        if e['type'] != 'Country':
            continue
        if ('disambiguated' in e) and ('name' in e['disambiguated']):
            countries.append(e['disambiguated']['name'])
        else:
            countries.append(e['text'])
    return countries

def getAnnotatedArticles():
    feedUrls = ['http://rss.cnn.com/rss/edition.rss',
                'http://rss.nytimes.com/services/xml/rss/nyt/World.xml',
                'http://feeds.bbci.co.uk/news/rss.xml',
                'http://www.aljazeera.com/Services/Rss/?PostingId=2007731105943979989']
    articles = []
    for feedUrl in feedUrls:
        notify("parsing " + feedUrl)
        feed = feedparser.parse(feedUrl)
        feed['entries'] = feed['entries'][0:20]
        for entry in feed['entries']:
            article = {
                'link': entry['link'],
                'title': entry['title'],
                'published': entry['published'],
                'sourceUrl': feedUrl,
                'source': feed['feed']['title']
            }
            notify("extracting keywords from " + entry['link'])
            article['keywords'] = extractKeywords(entry['link'])
            notify("extracting entities from " + entry['link'])
            article['entities'] = extractEntities(entry['link'])
            article['cities'] = citiesFromEntities(article['entities'])
            article['countries'] = countriesFromEntities(article['entities'])
            articles.append(article)
    return articles

os.chdir(os.path.dirname(sys.argv[0]))
f = open("../frontend/data/articles.js", "w")
f.write("var articles = " + json.dumps(getAnnotatedArticles()))
f.close()
