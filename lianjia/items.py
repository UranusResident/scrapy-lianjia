# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LianjiaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    url=Field()
    totalPrice=Field()
    roomType=Field()
    area=Field()
    unitPrice=Field()
    age=Field()
    decoration=Field()
    forward=Field()
    downPayment=Field()
    monthlyPayment=Field()
    court=Field()
    address=Field()
    floor=Field()
    lastTrade=Field()
    houseType=Field()
    houseTimelimit=Field()

    houseTypeImg=Field()

    region=Field()

    

