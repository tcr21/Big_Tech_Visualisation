import pytest

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pymongo
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv()

mongoDB = os.getenv('MONGODB_SERVER')
client = MongoClient(mongoDB)
db = client.visualising_news


def test_can_access_database():
    assert client.server_info()['ok'] == 1.0

def test_does_latest_data_contain_correct_fields():
    fields = ['_id', 'title', 'date', 'link', 'text', 'short_desc', 'publisher']
    latest_doc = db.raw_articles.find_one(sort=[( '_id', pymongo.DESCENDING )])

    for field in fields:
        assert latest_doc[field]

@pytest.fixture(scope='module')
def test_collection():
    print('SETUP TEST DATABASE')
    test_collection = db.test_collection
    yield test_collection
    print('TEARDOWN TEST DATABASE')
    test_collection.drop()

def test_can_add_to_a_database(test_collection):
    test_collection.insert_one({"test":"hello!"})
    assert test_collection.find_one(sort=[( '_id', pymongo.DESCENDING )])['test'] == "hello!"
    