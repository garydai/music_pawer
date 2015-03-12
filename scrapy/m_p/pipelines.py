# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy import log
import MySQLdb as mdb


class mysql_pipeline(object):

	def process_item(self, item, spider):

		cur  = self.conn.cursor(mdb.cursors.DictCursor)
		#for t in item:
		t = item
		url = t['url']
		song = t['song']
		singer = t['singer']
		source = t['source']
		d = t['date']
		sql = 'insert into music (url, song, singer, source,date) values ("%s", "%s", "%s", "%s", "%s")' % (url, song, singer, source, d)
		cur.execute(sql)
		self.conn.commit()

		
	
		return item

	def __init__(self):

		try:
			self.conn = mdb.connect(host=settings['SERVER'],
				user=settings['USER'],
				passwd=settings['PASSWORD'],
				db=settings['DB'],
				charset=settings['CHARSET'])

		        print "connet success"
		except mdb.Error, e:
			print "Mysql Error, %s,%s"%(e.args[0],e.args[1])


	
