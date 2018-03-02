# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Session(scrapy.Item):
    id = scrapy.Field()
    edition = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    tags = scrapy.Field()
    scheduled_at = scrapy.Field()
    location = scrapy.Field()
    language = scrapy.Field()
    level = scrapy.Field()
    speakers = scrapy.Field()
    type = scrapy.Field()

class Speaker(scrapy.Item):
    id = scrapy.Field()
    fullname = scrapy.Field()
    bio = scrapy.Field()
    country = scrapy.Field()
    personal_url = scrapy.Field()
    facebook = scrapy.Field()
    twitter = scrapy.Field()
    flickr = scrapy.Field()

