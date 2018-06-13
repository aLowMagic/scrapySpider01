# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapyspider01Item(scrapy.Item):
    title = scrapy.Field()
    abstract = scrapy.Field()
    main_body = scrapy.Field()
    originUrl = scrapy.Field()
    comments = scrapy.Field()
