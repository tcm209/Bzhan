# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BzhanItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass
class repliesItem(scrapy.Item):
    rpid=scrapy.Field
    count = scrapy.Field
    ctime = scrapy.Field
    floor = scrapy.Field
    like = scrapy.Field

    oid = scrapy.Field
    rcount = scrapy.Field
    device = scrapy.Field
    message = scrapy.Field
    displayRank = scrapy.Field
    avatar = scrapy.Field
    current_level = scrapy.Field

    mid = scrapy.Field
    uname = scrapy.Field
    rank = scrapy.Field
    sex = scrapy.Field
    sign = scrapy.Field
    pass
class BzhanX4(scrapy.Item):

    name = scrapy.Field()

    number =scrapy.Field()

    avid=scrapy.Field()

    username =scrapy.Field()

    userid = scrapy.Field()

    context =scrapy.Field()

    pass
