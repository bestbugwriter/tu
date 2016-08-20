# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs

class DuplicatesPipeline(object):
	def __init__(self):
		self.ids_seen = set()

	def process_item(self, item, spider):
		if item['image_urls'] is None:
			raise DropItem("none item found: %s" % item)
		else:
			#self.ids_seen.add(item['id'])
			return item

class JsonWriterPipeline(object):
	def __init__(self):
		self.file = open('items.json', 'wb')

	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + "\n"
		self.file.write(line)
		return item

class TuPipeline(object):
	def process_item(self, item, spider):
		#name = 'jinpai.html'
		self.outputHtml(item)
		return item
		
	i = 0

	def open_spider(self, spider):
		self.f = codecs.open('jinpai.html', 'wb', 'utf-8')
		self.f.write("<html>")
		self.f.write("<head>")
		self.f.write("<title>jinpai.html</title>")
		self.f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
		self.f.write("</head>")

		self.f.write("<body>")
		self.f.write("<table border=1 cellspacing=0 cellpadding=0 bordercolor=#000000>")

	def close_spider(self, spider):
		self.f.write("</table>")
		self.f.write("</body>")
		self.f.write("</html>")
		self.f.close()

	def outputHtml(self, item):
		try:
			self.i = self.i + 1
			self.f.write("<tr>")
			self.f.write("<td>%d</td>" %self.i)
			self.f.write("<td>%s</td>" %item['price'])
			self.f.write("<td>%s</td>" %item['houseType'])
			self.f.write("<td>%s</td>" %item['location'])
			self.f.write("<td>%s</td>" %item['config'])
			self.f.write("<td>%s</td>" %item['contact'])
			self.f.write("<td><a href=\"%s\">%s</a></td>" %(item['link'], item['brief']))
			self.f.write("<td><img width=\"100\" height=\"100\" src=\"%s\"></td>" %item['image_urls'][0])
			self.f.write("</tr>")
		except Exception as e:
			print("TuPipeline: outputHtml: " + str(e))

