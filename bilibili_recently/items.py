# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BilibiliRecentlyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'recently_submission'
    up = Field()
    up_href = Field()
    title = Field()
    describe = Field()
    video_href = Field()
    time = Field()
    log = Field()

