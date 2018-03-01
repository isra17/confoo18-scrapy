# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ConfooSpider(CrawlSpider):
    name = 'confoo2'
    allowed_domains = ['confoo.ca']
    start_urls = ['https://confoo.ca/en/yul2018/sessions']

    rules = (
        Rule(LinkExtractor(allow=r'/en/yul2018/session/'), callback='parse_session'),
    )

def parse_session(self, response):
    language, level = response.css('.well p')\
        .re(r'(\S+)\s+session\s+-\s+(\S+)')
    return {
        'id': response.url.strip('/').split('/')[-1],
        'title': response.css('h1::text').extract_first(),
        'summary': response.css('.e-description::text')\
            .extract_first()\
            .strip(),
        'tags': response.css('.well .tag::attr(class)')\
            .re(r":'([^']+)'\}"),
        'scheduled_at': datetime.strptime(
            ' '.join(response.css('.dt-date::text, .dt-time::text')\
                        .extract()),
            '%B %d, %Y %H:%M'),
        'location': response.css('.well .p-room::text').extract_first(),
        'language': language,
        'level': level,
        'speakers': response.css('.speakers .btn')\
            .xpath("./self::a[.='Read More']/@href")\
            .re('/([^/]+)$'),
    }

