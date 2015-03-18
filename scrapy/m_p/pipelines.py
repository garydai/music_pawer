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


		if item.has_key('url'):
			sql = 'select * from music  '
			cur.execute(sql)
			results = cur.fetchall()

		#for t in item:
			t = item
			url = t['url']
			song = t['song']
			singer = t['singer']
			source = t['source']
			d = t['date']
			album_id = ''
			if t.has_key('album_id'):
				album_id = t['album_id']
			exist = False;	
			for row in results:
		#	print row['song'],song

				if row['song'] == song:
		#		print row['song'],song

					sql = 'update music set date="%s" where id=%d' %(d, row['id'])
					if source == 'xiami':
						sql = 'update music set date="%s" , source="%s", album_id="%s" , url="%s" where id=%d' %(d, source, album_id, url, row['id'])

					cur.execute(sql)
					self.conn.commit()

					exist = True
			if not exist:
				sql = 'insert into music (url, song, singer, source, date, album_id) values ("%s", "%s", "%s", "%s", "%s", "%s")' % (url, song, singer, source, d, album_id)
				cur.execute(sql)
				self.conn.commit()


		else:

			sql = 'select count(*) from comment where tag = "%s" ' % (item['tag'])
			
                        cur.execute(sql)
                        results = cur.fetchone()
			if results['count(*)'] == 0:

				sql = 'insert into comment (album_id, comment, tag) values ("%s", "%s", "%s")' %(item['album_id'], item['comment'], item['tag'])
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


	
