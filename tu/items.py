#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field

class TuItem(Item):
	price = Field()
	houseType = Field()
	location = Field()
	brief = Field()
	link = Field()
	config = Field()
	contact = Field()
	pass
