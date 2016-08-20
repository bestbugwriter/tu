#!/usr/bin/python3

# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from tu.items import TuItem
from tu.pipelines import TuPipeline
import sys
import re
import string
#sys.stdout=open('output.txt','w')

class TuSpider(CrawlSpider):
	name = "tu"
	allowed_domains = ["58.com"]
	#ab = lambda x: "http://hz.58.com/zufang/pn" + str(x) + "/"
	#start_urls = [(lambda x: "http://hz.58.com/zufang/pn" + str(x) + "/") for x in range(0,1)]
	start_urls = ["http://hz.58.com/zufang/pn1/".encode('utf8'), "http://hz.58.com/zufang/pn2/".encode('utf8')]

	rules = (
		Rule(SgmlLinkExtractor(allow=('hz.58.com/pinpaigongyu/.*', )), callback='parse_pp'),
		Rule(SgmlLinkExtractor(allow=('short.58.com/', )), callback='parse_gold'),
		Rule(SgmlLinkExtractor(allow=('jinpai.58.com/', )), callback='parse_gold'),
		Rule(SgmlLinkExtractor(allow=('hz.58.com/zufang/.*', )), callback='parse_gold'),
		)

	def wash_data(self, data):
		data = re.sub("\n", " ", data)
		data = re.sub("\r", " ", data)
		data = re.sub("\t", " ", data)
		data = re.sub(" ", "", data)
		return data

	def parse_gold(self, response):
		sel = Selector(response)
		items = []
		item = TuItem()

		try:
			l = sel.xpath('//ul[@class="house-primary-content"]/li[1]/div[@class="fl"]//text()').extract()
			item['price'] = self.wash_data(''.join(l)).encode('utf8')

			l = sel.xpath('//ul[@class="house-primary-content"]/li[2]//text()').extract()
			item['houseType'] = self.wash_data(''.join(l)).encode('utf8')

			l = sel.xpath('//ul[@class="house-primary-content"]/li[3]//text()').extract()
			item['location'] = self.wash_data(''.join(l)).encode('utf8')

			l = sel.xpath('//ul[@class="house-primary-content"]/li[4]//text()').extract()
			item['config'] = self.wash_data(''.join(l)).encode('utf8')

			l = sel.xpath('//div[@class="fl tel cfff"]//text()').extract()
			item['contact'] = self.wash_data(''.join(l)).encode('utf8')

			l = sel.xpath('//img[@id="smainPic"]/@src')
			#if len(l) > 0:
			item['image_urls'] = l.extract()
			item['images'] = l.re(r'[^/]*.[jpg|png|gif]$')
			#print(item['image_urls'])

			item['brief'] = sel.xpath('//h1[1]//text()').extract()[0].encode('utf-8')
			item['link'] = response.url.encode('utf-8')

			items.append(item)
			#print(type(item))
			#print(item)
		except Exception as e:
			print("parse_gold: xpath error: " + str(e))
			pass

		return items


	def parse_pp(self, response):
		sel = Selector(response)
		items = []
		item = TuItem()

		try:
			l = sel.xpath('//div[@class="house-title center cf"]/div[@class="detail_header"]//text()')
			item['price'] = self.wash_data(''.join(l)).encode('utf8')

			l = sel.xpath('//ul[@class="house-info-list"]/li[2]//text()')
			item['houseType'] = self.wash_data(''.join(l)).encode('utf8')

			l = sel.xpath('//ul[@class="house-info-list"]/li[4]//text()')
			item['location'] = self.wash_data(''.join(l)).encode('utf8')

			l = sel.xpath('//div[@class="tags"]/ul[@class="tags-list"]//text()')
			item['config'] = self.wash_data(''.join(l)).encode('utf8')

			l = sel.xpath('//div[@class="detail_headercon"]/div[@class="phonenum"]//text()')
			item['contact'] = self.wash_data(''.join(l)).encode('utf8')

			l = sel.xpath('//div[@class="house-title-wrap"]/img/@src')
			#if len(l) > 0:
			
			item['image_urls'] = l.extract()
			item['images'] = l.re(r'[^/]*.[jpg|png|gif]$')

			item['brief'] = sel.xpath('//h2//text()').extract()[0].encode('utf8')
			item['link'] = response.url.encode('utf-8')
			items.append(item)

		except Exception as e:
			print("parse_pp: xpath error: " + str(e))
			pass
		return items
