# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from scrapy import Request, Spider
from lxml import etree

from bilibili_recently.items import BilibiliRecentlyItem


class BilibiliSpider(Spider):
    name = 'bilibili'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['http://www.bilibili.com/']

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    url = 'https://www.bilibili.com/v/game/esports/?'
    query = {'spm_id_from':'333.8.game_esports.17'}

    def start_requests(self):
        for pn in range(1, self.settings.get('MAX_PN')+1):
            url = self.url+urlencode(self.query)
            yield Request(url=url, headers=self.headers, meta={'pn': pn}, callback=self.parse_recently, dont_filter=True)

    def parse_recently(self, response):
        videos = response.xpath('//div[@id="videolist_box"]/div[2]/ul[contains(@class,"vd-list")]//li//div[@class="r"]')
        for video in videos:
            item = BilibiliRecentlyItem()
            item['up'] = video.css('div.up-info > a::text').extract_first()
            item['up_href'] = 'https:' + video.css('div.up-info > a::attr("href")').extract_first()
            item['title'] = video.css('a::text').extract_first()
            item['describe'] = video.css('div.v-desc::text').extract_first().replace('\n','')
            item['video_href'] = 'https:' + video.css('a::attr("href")').extract_first()
            yield item
            video_url = item.get['video_href']
            yield Request(url=video_url, headers=self.headers, callback=self.parse_video)

    def parse_video(self, response):
        pass



