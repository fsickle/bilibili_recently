# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from scrapy import Request, Spider
from lxml import etree
import time
from bilibili_recently.items import BilibiliRecentlyItem
from logging import getLogger


class BilibiliSpider(Spider):
    name = 'bilibili'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['http://www.bilibili.com/']

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q = 0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN, zh;q = 0.9',
        'Cache - Control': 'max-age = 0',
        'Connection': 'keep-alive',
        'Host': 'www.bilibili.com',
    }
    url = 'https://www.bilibili.com/v/game/esports/'
    logger = getLogger(__name__)

    def start_requests(self):
        for pn in range(1, self.settings.get('MAX_PN')+1):
            yield Request(url=self.url, headers=self.headers, meta={'pn': pn}, callback=self.parse_recently, dont_filter=True)

    def parse_recently(self, response):
        '''
        对主页面进行解析，得到 video 的 url
        :param response: middleware 的返回
        :return: 对每个 video 的请求
        '''
        videos = response.xpath('//div[@id="videolist_box"]/div[2]/ul[contains(@class,"vd-list")]//li//div[@class="r"]')
        for video in videos:
            video_url = 'https:' + video.css('a::attr("href")').extract_first()
            #self.logger.debug(video_url)
            time.sleep(0.5)
            yield Request(url=video_url, headers=self.headers, callback=self.parse_video)

    def parse_video(self, response):
        # 对 video 进行解析，并复制 Item
        item = BilibiliRecentlyItem()

        #新版播放器界面的解析
        # item['up'] = response.css('#v_upinfo > div.u-info > div > a.username::text').extract_first()
        # item['up_href'] = 'https:' + response.css('#v_upinfo > div.u-info > div > a.username::attr("href")').extract_first()
        # item['title'] = response.css('#viewbox_report > h1 > span::text').extract_first()
        # describe = response.css('#v_desc > div::text').extract_first()
        # if describe:
        #     item['describe'] = describe.replace('\n', '')
        # else:
        #     item['describe'] = 'None'
        # item['video_href'] = response.url
        # item['time'] = response.css('#viewbox_report > div > time::text').extract_first()
        # logs = []
        # for log in response.css('#v_tag > ul > li'):
        #     logs.append(log.css('a::text').extract_first())
        # item['logs'] = logs
        # yield item

        #旧版播放器界面的解析
        item['up'] = response.css('v_upinfo > div.info > div.user.clearfix > a.name::text').extract_first()
        item['up_href'] = 'https:' + response.css('#v_upinfo > div.info > div.user.clearfix > a.name::attr("href")').extract_first()
        item['title'] = response.css('#viewbox_report > h1 > span::text').extract_first()
        describe = response.css('#v_desc > div.info.open::text').extract_first()
        if describe:
            item['describe'] = describe.replace('\n', '')
        else:
            item['describe'] = 'None'
        item['video_href'] = response.url
        item['time'] = response.css('#viewbox_report > div.tm-info.tminfo > time::text').extract_first()
        logs = []
        for log in response.css('#v_tag > ul > li'):
            logs.append(log.css('a::text').extract_first())
        item['logs'] = logs
        yield item





