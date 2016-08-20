
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi			  #导入twisted的包
import MySQLdb
import MySQLdb.cursors
#import pymysql
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




class MySQLPipeline(object):
	def __init__(self):							#初始化连接mysql的数据库相关信息
		self.cur, self.conn = self.initDBTable()

	insert = "insert into %s (price, houseType, location, brief, link, config, contact, image_urls) values (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")"
	createTable = "create table %s (id int auto_increment not null primary key, price TEXT(512), houseType TEXT(512), location TEXT(512), brief TEXT(512), link TEXT(512), config TEXT(512), contact TEXT(512), image_urls TEXT(512))"

	def initDBTable(self):
		DBName = 'tu'
		TableName = 'tu2'
		conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='toor',db='mysql',charset='utf8')
		cur = conn.cursor()
		cur.execute("USE %s" %DBName)
		print(cur.fetchall())
		DB1 = (TableName,)
		cur.execute('show tables')
		aa = cur.fetchall()
		print(DB1, aa)
		if DB1 not in aa:
			cur.execute(self.createTable %TableName)

			cur.execute("ALTER DATABASE %s CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci" % DBName)
			#cur.execute("ALTER TABLE %s CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci" % TableName)  
			cur.execute("ALTER TABLE %s CHANGE title title VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci" % TableName)
			cur.execute("ALTER TABLE %s CHANGE content content VARCHAR(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci" % TableName)
			
		cur.execute("describe %s" %TableName)
		print(cur.fetchall())
		return cur, conn

	# pipeline dafault function					#这个函数是pipeline默认调用的函数
	def process_item(self, item, spider):
		try:
			self.cur.execute(self.insert %("tu2", item['price'], item['houseType'], item['location'], item['brief'], item['link'], item['config'], item['contact'], item['image_urls'][0]))
			print("insert data success.")
		except Exception as e:
			print("MySQLPipeline: " + str(e))

		return item

	def close_spider(self, spider):
		print("close mysql.")
		self.cur.close()
		self.conn.close()

	# insert the data to databases				 #把数据插入到数据库中
	def _conditional_insert(self, tx, item):
		p=open('yeah.txt','a')
		p.write(str(item["link"]))
		sql = "insert into book values (%s, %s)"
		tx.execute(sql,(item["title"][0:], item["link"][0:]))