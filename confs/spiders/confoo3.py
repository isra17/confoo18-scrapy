# -*- coding: utf-8 -*-
import re
import scrapy
from confs.items import Session, Speaker
from itertools import chain
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


SOCIAL_URL_RE = re.compile(r'://([^.]+).+/([^/]+)$')


class ConfooSpider(CrawlSpider):
    name = 'confoo3'
    allowed_domains = ['confoo.ca']
    start_urls = [
        'https://confoo.ca/en/yul2018/sessions',
        'https://confoo.ca/en/yul2018/speakers',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/en/yul2018/session/'), callback='parse_session', follow=True),
        Rule(LinkExtractor(allow=r'/en/speaker/'), callback='parse_speaker', follow=True),
    )

    def parse_session(self, response):
        session_info = response.css('.well p')\
            .re(r'(\S+)\s+session\s+-\s+(\S+)')
        if not session_info:
            self.logger.info(f'Skipping training {response.url}.')
            return # Skip training
        language, level = session_info

        date_parts = response.css('.dt-date::text, .dt-time::text').extract()
        scheduled_at = None
        if date_parts:
            datetime.strptime(' '.join(date_parts, '%B %d, %Y %H:%M'))

        yield Session(
            id=response.url.strip('/').split('/')[-1],
            title=response.css('h1::text').extract_first(),
            summary=response.css('.e-description::text')\
                .extract_first()\
                .strip(),
            tags=response.css('.well .tag::attr(class)')\
                .re(r":'([^']+)'\}"),
            scheduled_at=,
            location=response.css('.well .p-room::text').extract_first(),
            language=language,
            level=level,
            speakers=response.css('.speakers .btn')\
                .xpath("./self::a[.='Read More']/@href")\
                .re('/([^/]+)$'),
        )

    def parse_speaker(self, response):
        # Flatmap all url into (site,username) and create a dict from them.
        social = dict(
            filter(
                lambda i: i[0] in ('twitter', 'facebook', 'flickr'),
                chain.from_iterable(
                    map(SOCIAL_URL_RE.findall,
                        response.css('.well a[title]::attr(href)').extract()))))

        yield Speaker(
            id=response.url.strip('/').split('/')[-1],
            fullname=response.css('h1::text').extract_first(),
            bio=response.css('.speaker > p::text').extract_first().strip(),
            country=response.css('.well .flag-icon::attr(title)').extract_first(),
            personal_url=response.css('.well a:not([title])::attr(href)').extract_first(),
            **social
        )
