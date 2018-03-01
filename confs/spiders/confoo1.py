# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ConfooSpider(CrawlSpider):
    name = 'confoo'
    allowed_domains = ['confoo.ca']
    start_urls = ['http://confoo.ca/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        return i

