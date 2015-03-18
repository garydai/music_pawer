# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field

class MusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	song = Field()
	url = Field()
	singer = Field()
	source = Field()
	date = Field()
	image = Field()
	discuss = Field()
	album_id = Field()	

class commentItem(scrapy.Item):
	
	album_id = Field()
	comment = Field()
	singer = Field()
	song = Field()
	tag = Field()

