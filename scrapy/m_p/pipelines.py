# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.conf import settings
from scrapy import log
import MySQLdb as mdb
import urllib
import time
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class mysql_pipeline(object):



	#最好并行下载,需要一个下载图片的任务	
	def getImage(self, url, save_image):

		
		
		data = urllib.urlopen(url).read()  
		f = file(save_image,"wb")  
		f.write(data)  
		f.close() 


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
			image = t['image']
			postfix = image
			#postfix = source + str(int(time.time())) + '.jpg'	
#			save_image = '/home/admin/nginx/html/yii/demos/music_web/images/cover/' + source + str(int(time.time())) + '.jpg'
#			print save_image
	#		self.getImage(image, save_image)
			
			album_id = ''
			if t.has_key('album_id'):
				album_id = t['album_id']
			exist = False;	
			for row in results:
		#	print row['song'],song

				if row['song'] == song and row['singer'] == singer:
		#		print row['song'],song

					sql = 'update music set date="%s", url="%s", source="%s", album_id="%s" where id=%d' %(d, url, source, album_id, row['id'])


					
					#更新来源xiami，因为它有评论
					#if source == 'xiami':
					#	sql = 'update music set date="%s" , image="%s", source="%s", album_id="%s" , url="%s" where id=%d' %(d, postfix, source, album_id, url, row['id'])

					cur.execute(sql)
					self.conn.commit()

					exist = True
					break
				
			if not exist:
				sql = 'insert into music (image, url, song, singer, source, date, album_id) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (postfix, url, song, singer, source, d, album_id)
				cur.execute(sql)
				self.conn.commit()
			else:
				raise DropItem("has existed item  %s" % item)

		##评论

		else:

			sql = 'select count(*) from other_comment where tag = "%s" ' % (item['tag'])
			
                        cur.execute(sql)
                        results = cur.fetchone()
			if results['count(*)'] == 0:

				sql = 'insert into other_comment (album_id, comment, tag) values ("%s", "%s", "%s")' %(item['album_id'], item['comment'], item['tag'])
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





class download_image_pipeline(ImagesPipeline):


	def get_media_requests(self, item, info):

		if item.has_key('url'):

			image_url = item['image']
			yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):


		if item.has_key('url'):

			image_paths = [x['path'] for ok, x in results if ok]
			if not image_paths:
				raise DropItem("Item contains no images")
			item['image'] = image_paths[0]
		return item


	
