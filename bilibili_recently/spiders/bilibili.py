# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from scrapy import Request, Spider

class BilibiliSpider(Spider):
    name = 'bilibili'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['http://www.bilibili.com/']

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    url = 'https://www.bilibili.com/v/game/esports/?'
    query = 'spm_id_from:333.8.game_esports.17'

    def start_requests(self):
        for pn in range(1, self.settings.get('MAX_PN')+1):
            yield Request(self.url+urlparse(self.query), headers=self.headers, meta={'pn': pn}, callback=self.parse_recently, dont_filter=True)

    def parse_recently(self, response):
        print(response.text)
