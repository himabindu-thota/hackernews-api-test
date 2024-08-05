"""This module provides API acceptance tests for our hacker news app"""

from hn_app import get_top_stories, get_current_top_story
from hn_app import get_story, get_story_comment
import pytest
import requests

### API reachable ###

def test_api_reachable():
    resp_top = get_top_stories("https://abcdefnonexisting")
    assert 'error' in resp_top.keys()

### Top Stories Acceptance Tests ###

def test_get_top_stories_status_code_200():
    resp_top = get_top_stories()
    assert resp_top.status_code == 200

def test_get_top_stories_count_500():
    resp_top = get_top_stories()
    assert len(resp_top.json()) == 500

### Current Top Story Acceptance Tests ###

def test_get_current_top_story_status_code_200():
    resp_cur_top = get_current_top_story()
    assert resp_cur_top.status_code == 200

def test_get_current_top_story_comments_field():
    resp_cur_top = get_current_top_story()
    data = resp_cur_top.json()
    assert isinstance(data.get('kids', []), list)

def test_required_field_id():
    resp_cur_top = get_current_top_story()
    data = resp_cur_top.json()
    assert data.get('id', None) is not None

def test_type_field_story():
    resp_cur_top = get_current_top_story()
    data = resp_cur_top.json()
    assert data.get('type', None) == 'story'

def test_story_by_field_present():
    resp_cur_top = get_current_top_story()
    data = resp_cur_top.json()
    assert data.get('by', None) is not None

def test_story_by_field_not_empty():
    resp_cur_top = get_current_top_story()
    data = resp_cur_top.json()
    assert data.get('by', None) != ""

@pytest.mark.xfail(returns=200)
def test_get_story_with_non_integer_story_id_status_code_400_1():
    resp = get_top_stories()
    data = resp.json()
    story_id = str(data[5])
    story_id += "!"
    resp = get_story(story_id)
    assert resp.status_code == 400

@pytest.mark.xfail(returns=None)
def test_get_story_with_non_integer_story_id_1():
    resp = get_top_stories()
    data = resp.json()
    story_id = str(data[5])
    story_id += "!"
    resp = get_story(story_id)
    assert isinstance(resp.json(), dict)

@pytest.mark.xfail(returns=200)
def test_get_story_with_non_integer_item_id_status_code_400_2():
    resp = get_top_stories()
    data = resp.json()
    story_id = str(data[5])
    story_id += "#"
    resp = get_story(story_id)
    assert resp.status_code == 400

@pytest.mark.xfail(raises=requests.exceptions.JSONDecodeError)
def test_get_story_with_non_integer_item_id_2():
    resp = get_top_stories()
    data = resp.json()
    story_id = str(data[5])
    story_id += "#"
    resp = get_story(story_id)
    #assert resp.status_code == 200
    #with pytest.raises(requests.exceptions.JSONDecodeError):
    assert isinstance(resp.json(), dict)

### Story Comment Acceptance Tests ###

def test_comment_should_have_a_parent():
    resp = get_top_stories()
    data = resp.json()
    story_id = str(data[0])
    resp = get_story_comment(story_id)
    data = resp.json()
    assert data.get('parent', None) is not None

def test_comment_should_have_a_text():
    resp = get_top_stories()
    data = resp.json()
    story_id = str(data[0])
    resp = get_story_comment(story_id)
    data = resp.json()
    assert data.get('text', None) is not None

def test_comment_should_have_type_comment():
    resp = get_top_stories()
    data = resp.json()
    story_id = str(data[0])
    resp = get_story_comment(story_id)
    data = resp.json()
    assert data.get('type') == 'comment'

def test_comment_by_field_present():
    resp = get_top_stories()
    data = resp.json()
    story_id = str(data[0])
    resp = get_story_comment(story_id)
    data = resp.json()
    assert data.get('by', None) is not None

def test_comment_by_field_not_empty():
    resp = get_top_stories()
    data = resp.json()
    story_id = str(data[0])
    resp = get_story_comment(story_id)
    data = resp.json()
    assert data.get('by', None) != ""

### Get all 500 stories in top stories one at a time ###
@pytest.mark.burst
def test_get_all_top_stories_and_iterate():
    print('\n\n *** NOTE: This test takes about 2 mins to complete. ' + \
           'To skip next time use -m "not burst" flag')
    resp_top = get_top_stories()
    assert resp_top.status_code == 200
    for story_id in resp_top.json():
        resp_story = get_story(story_id)
        assert resp_story.status_code == 200    
