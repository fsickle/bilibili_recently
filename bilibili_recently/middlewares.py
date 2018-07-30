# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals



class BilibiliRecentlySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BilibiliRecentlyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from logging import getLogger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
import re
from selenium.webdriver.chrome.options import Options
import requests

class SeleniumMiddleware():
    def __init__(self, timeout=None,proxy_pool_url=None):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.proxy_pool_url = proxy_pool_url
        self.proxy = self.get_proxy()
        self.chrome_options.add_argument('proxy-server='+ self.proxy)
        self.brower = webdriver.Chrome(chrome_options=self.chrome_options)
        self.wait = WebDriverWait(self.brower, timeout=self.timeout)

    def get_proxy(self):
        try:
            response = requests.get(self.proxy_pool_url)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    def __del__(self):
        self.brower.close()

    def process_request(self, request, spider):
        '''
        用 Chrome 抓取页面
        :param request: Request 对象
        :param spider: Spider 对象
        :return: HtmlResponse
        '''
        self.logger.debug('chrome is starting')
        result = re.search('com/video/av', request.url)
        if result:
            return None
        pn = request.meta.get('pn', 1)
        try:
            self.brower.get(request.url)
            if pn > 1:
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#videolist_box > div.vd-list-cnt > div.pager.pagination > div > input')))
                input.clear()
                input.send_keys(pn)
                input.send_keys(Keys.ENTER)
            self.wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#videolist_box > div.vd-list-cnt > div.pager.pagination > ul > li.page-item.active > button'), str(pn)))
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#videolist_box > div.vd-list-cnt > ul > li > div > div.r')))
            return HtmlResponse(url=request.url, body=self.brower.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url,status=500,request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   proxy_pool_url=crawler.settings.get('PROXY_POOL_URL'))

class VideoMiddleware():
    def __init__(self, timeout=None,proxy_pool_url=None):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.proxy_pool_url = proxy_pool_url
        self.proxy = self.get_proxy()
        self.chrome_options.add_argument('proxy-server=' + self.proxy)
        self.chrome_options.add_argument('proxy-server='+ self.proxy)
        self.brower = webdriver.Chrome(chrome_options=self.chrome_options)
        self.wait = WebDriverWait(self.brower, timeout=self.timeout)

    def get_proxy(self):
        try:
            response = requests.get(self.proxy_pool_url)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    def __del__(self):
        self.brower.close()

    def process_request(self, request, spider):
        '''
        用 Chrome 抓取页面
        :param request: Request 对象
        :param spider: Spider 对象
        :return: HtmlResponse
        '''
        self.logger.debug('video is starting')
        try:
            self.brower.get(request.url)
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div > div.player-box')))
            return HtmlResponse(url=request.url, body=self.brower.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url,status=500,request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   proxy_pool_url=crawler.settings.get('PROXY_POOL_URL'))


