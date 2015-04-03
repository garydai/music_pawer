#coding:utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from bs4 import BeautifulSoup
from m_p.items import *
from datetime import *
import urllib
from scrapy.http import Request
import json
import re
class MusicSpider(BaseSpider):
	name = 'music'
	allowed_domains = []
	start_urls = ['http://y.qq.com/y/static/index.html', 'http://www.xiami.com', 'http://music.163.com/discover']
  

#	start_urls = ['http://music.163.com/api/v1/resource/comments/R_AL_3_3104053/?rid=R_AL_3_3104053&offset=0&total=true&limit=20&csrf_token=']

	def parse(self, response):
#		print response.url
#		print response.body

		if response.url == 'http://y.qq.com/y/static/index.html':
		#if response.url == 'http://y.qq.com/y/static/recom/song.js?loginUin=0&hostUin=0&format=jsonp&inCharset=GB2312&outCharset=utf-8&notice=0&platform=yqq&jsonpCallback=MusicJsonCallback&needNewCode=0':
			return self.parseQQ(response)

		elif response.url == 'http://www.xiami.com':

			return self.parseXiami(response)

		elif response.url == 'http://music.163.com/discover':

                        return self.parse163(response)


	def parseQQ(self, response):

		'''	
		#print response.body	
		text = response.body
		index1 = text.find('(')
		index2 = text.rfind(')')
		text = text[index1 +1: index2]
#		print text
		text = text.replace('"', "'")
		text = re.sub(r":'(.+?)',", ":\"\\1\",", text)
 
		print text	
		text1 = re.sub(r"(,?)(\w+?)\s*?:", "\\1\"\\2\":", text)
		#text1 = text1.replace("'", '"');
		print text1
		j = json.loads(text1, 'utf-8')
#
		print j	


		'''	
		soup = BeautifulSoup(response.body)
		items = []
                #now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		qq_new  = soup.find('ul', {'class':'mod_first_list'})

#       print qq_new
		for x in qq_new.find_all('li'):


			m_item = MusicItem()

			a = x.find('a',{'class':'mod_poster_130'})

			url = 'http://y.qq.com' + a.get('href')
		#	print 'song_url', 'http://y.qq.com' + a.get('href')
			em = x.find('strong', {'class':'album_name'})
			song =   em.contents[0]
		#	print 'song', em.contents[0].encode('utf8')
			em = x.find('strong', {'class':'album_singer'})
			singer =  em.contents[0]
		#	print 'singer', em.contents[0].encode('utf8')


			cover_div = x.find('a').find('img').get('_src')


			m_item['song'] = song
			m_item['url'] = url
			m_item['singer'] = singer
			m_item['source'] = u'QQ'
			now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			m_item['date'] = now
			m_item['image'] = cover_div
			items.append(m_item)
		
			
		return items

	def parseXiami(self, response):
	
		soup = BeautifulSoup(response.body)

		
		xiami_new       = soup.find('div', {'id':'albums'})
#       print xiami_new
		info = xiami_new.find('div',{'class':'album'})
        #print info
		a = info.find('div',{'class':'info'})
		p = a.find_all('p')

		items = []

		url = 'http://www.xiami.com' +p[0].find('a').get('href')
		song =  p[0].find('a').string
		singer =  p[1].find('a').string
		source = u'xiami'
		#print 'song_url' , 'http://www.xiami.com' +p[0].find('a').get('href')
		#print 'song', p[0].find('a').string.encode('utf8')
		#print 'singer', p[1].find('a').string.encode('utf8')	
		m_item = MusicItem()
		m_item['song'] = song
		m_item['url'] = url
		m_item['singer'] = singer
		m_item['source'] = source
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		m_item['date'] = now
		items.append(m_item)

		yield Request(url, callback=self.parse_xiami_discuss)
		
		for sibling in info.next_siblings:
                #print(repr(sibling))
                #break
			if(sibling !=' ' ):
				a = sibling.find('div',{'class':'info'})
				p = a.find_all('p')
                        #print p
				url = 'http://www.xiami.com' +p[0].find('a').get('href')
				items.append(m_item)
				yield Request(url, callback=self.parse_xiami_discuss)



#		yield items

	
				

	def parse_xiami_discuss(self, response):


		soup  = BeautifulSoup(response.body)

		div_singer = soup.find('div', {'id':'album_info'})
		singer = div_singer.find('tr').find('a').string

		div_album = soup.find('div', {'id':'album_cover'})
		song = div_album.find('a').get('title')
		image = div_album.find('a').find('img').get('src')
		m_item = MusicItem()
		m_item['song'] = song
		m_item['url'] = response.url
		m_item['singer'] = singer
		m_item['source'] = u'xiami'
		m_item['image'] = image

	#	postfix = source + str(int(time.time())) + '.jpg'
	#	save_image = '/home/admin/nginx/html/yii/demos/music_web/images/cover/' + postfix
	#	print save_image
	#	callback = lambda response: self.getImage(response, image, postfix)

	#	yield Request(image,)	
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		id = response.url.rfind('/')
		album_id = response.url[id + 1:]
		m_item['album_id'] = album_id	
		m_item['date'] = now
#		yield Request('http://www.xiami.com/commentlist/turnpage/id/'+album_id+'/page/1/ajax/1?type=1', callback=self.parse_xiami_comment)

		yield m_item
#		print 111111111111111111111111111111111111111111111111111111111111111


	def parse_xiami_comment(self, response):
		
		soup  = BeautifulSoup(response.body)
		div = soup.findAll('div', {'class':'brief'})
		for d in div:
			if d.find('div').string != None:
				m_item = commentItem()
				m_item['comment'] = d.find('div').string
				m_item['tag'] = d.find('div').get('id')
				index1 = response.url.find('id/')
				index2 = response.url.find('/page')
				
				m_item['album_id'] = response.url[index1+3:index2]
				yield m_item

		if response.body.find('下一页') != -1:
			url = response.url
			index1 = response.url.find('/page/')
			index2 = response.url.find('/ajax')
			id = int(url[index1+6:index2])
			id += 1
			
			url = response.url[:index1] + '/page/' + str(id) + '/ajax/1?type=1'
			#print url
			yield Request(url, callback=self.parse_xiami_comment)

			#print '-----------------'






	def parse163(self, response):

		soup = BeautifulSoup(response.body)

        #print text
		a       = soup.find('div', {'class':'roll f-pr'})
		
        #print a
		items = []
		for x in a.find_all('li'):

			p = x.find_all('p')


			url = 'http://music.163.com/#' +p[0].find('a').get('href')
			album_id = url[url.find('id=')+3:]

			song =  p[0].find('a').string
			singer =  p[1].find('a').string
			source = '163'

	
			
		#	print 'song_url' , 'http://music.163.com/#' +p[0].find('a').get('href')
		#	print 'song', p[0].find('a').string.encode('utf8')
		#	print 'singer', p[1].find('a').string.encode('utf8')


			m_item = MusicItem()
			m_item['song'] = song
			m_item['url'] = url
			m_item['singer'] = singer
			now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			m_item['source'] = source
			m_item['date'] = now
			m_item['album_id'] = album_id			
			cover_div = x.find('div', {'class':'u-cover u-cover-alb1'}).find('img').get('data-src')
			m_item['image'] = cover_div

			items.append(m_item)

		return items




		#sel = Selector(response)
		#sites = sel.xpath('//td[@class="title"]')
		#for site in sites:
	#	title = site.xpath('a/text()').extract()
	#	link = site.xpath('a/@href').extract()
  

		#print title, link



