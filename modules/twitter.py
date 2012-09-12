#!/usr/bin/env python

#Project: Taeniurus irc bot  https://github.com/s1n4/Taeniurus
#Twitter module for the Taeniurus bot to read the last tweet of of a twitter user

import json
import urllib


def tweet(username=None):
    if not username: username = '_s1n4_'
    if type(username) is list: username = str(username[0])
    twitter_url = 'http://api.twitter.com/1/statuses/user_timeline.json?screen_name=%s&include_rts=true' % username
    jsonFile = urllib.urlopen(twitter_url)
    return username + ': ' + json.load(jsonFile)[0]['text']
