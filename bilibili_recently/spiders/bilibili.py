# -*- coding: utf-8 -*-
import scrapy


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['http://www.bilibili.com/']

    def parse(self, response):
        pass
