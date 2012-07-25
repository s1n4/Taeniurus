#!/usr/bin/env python

#Project: Taeniurus irc bot  https://github.com/s1n4/Taeniurus
#Twitter module for the Taeniurus bot

import json, urllib


def tweet(username=None):
    if not username: username = '_s1n4_'
    if type(username) is list: username = str(username[0])
    twitterUrl = 'http://api.twitter.com/1/statuses/user_timeline.json?screen_name=%s&include_rts=true' % username
    jsonFile = urllib.urlopen(twitterUrl)
    return username + ': ' + json.load(jsonFile)[0]['text']

