"""This module provides our simple hacker news app"""

import requests
import pytest

def get_top_stories(url=None):
    """Fetch top stories from the URL"""
    if url is None:
        url = "https://hacker-news.firebaseio.com/v0/" + \
              "topstories.json?print=pretty"
    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        return {'error':str(e)}
    return resp

def get_story(story_id):
    """Fetch story detail. Uses items api"""
    url = "https://hacker-news.firebaseio.com/v0/item/"+ \
           str(story_id)+".json?print=pretty"
    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        return {'error':str(e)}
    return resp

def get_current_top_story():
    """Fetch current top story"""
    resp = get_top_stories()
    data = resp.json()
    top_story_id = data[0]
    resp = get_story(top_story_id)
    return resp

def get_story_comment(story_id, comment_rank=1):
    """Fetch the top comment by default for a given story"""
    resp = get_story(story_id)
    data = resp.json()
    if data.get('kids', None) is not None:
        comment_id = data.get('kids')[comment_rank-1]
        url = "https://hacker-news.firebaseio.com/v0/item/"+ \
               str(comment_id)+".json?print=pretty"
        try:
            resp = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            return {'error':str(e)}
        return resp
    return ''
