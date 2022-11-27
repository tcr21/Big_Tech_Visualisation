# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from os import link
import scrapy

# TODO am I right in thinking that this can just be deleted because it was part of the tutorial @justin?
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


def remove_whitespace(value):
    return value.strip()


class BaseArticlesItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    text = scrapy.Field()
    short_desc = scrapy.Field()
    publisher = scrapy.Field()


class BBCArticlesItem(BaseArticlesItem):
    pass


class GuardianArticlesItem(BaseArticlesItem):
    pass


class AndreessenHorowitzArticlesItem(BaseArticlesItem):
    pass


class ZDNetArticlesItem(BaseArticlesItem):
    pass
