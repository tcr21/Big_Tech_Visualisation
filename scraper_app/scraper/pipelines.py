# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

from scrapy import settings
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

# useful for handling different item types with a single interface, currently unused
from itemadapter import ItemAdapter

settings = get_project_settings()

# TODO logging for the pipeline would be really nice


class DuplicatesPipeline:
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(settings["MONGODB_SERVER"])
        self.collection = self.connection.visualising_news.raw_articles

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # TODO consider whether to ignore this item or replace the old one. Link here:
        # "upsert" option for replace_one: https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html
        if self.collection.count_documents({"link": item["link"]}, limit=1):
            raise DropItem(f"Duplicate item found: {item!r}")
        return item


class MongoPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(settings["MONGODB_SERVER"])
        self.collection = self.connection.visualising_news.raw_articles

    def close_spider(self, spider):
        self.connection.close()

    # TODO could do with a quick refactoring
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert_one(dict(item))
            print("I added something!")

        return item
