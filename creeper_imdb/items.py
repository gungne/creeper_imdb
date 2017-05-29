# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    identifier = scrapy.Field()
    title = scrapy.Field()
    publish_date = scrapy.Field()
    director  = scrapy.Field()
    creator = scrapy.Field()
    cast = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    review_info  = scrapy.Field()


# class ImdbReviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	