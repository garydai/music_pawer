from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from bs4 import BeautifulSoup
from m_p.items import MusicItem
from datetime import *
class MusicSpider(BaseSpider):
	name = 'music'
	allowed_domains = []
	start_urls = ['http://y.qq.com/y/static/index.html', 'http://www.xiami.com', 'http://music.163.com/discover']
  
	def parse(self, response):
		print response.url


		if response.url == 'http://y.qq.com/y/static/index.html':

			return self.parseQQ(response)

		elif response.url == 'http://www.xiami.com':

			return self.parseXiami(response)

		elif response.url == 'http://music.163.com/discover':

                        return self.parse163(response)


	def parseQQ(self, response):

		soup = BeautifulSoup(response.body)
		items = []
                #now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		qq_new  = soup.find('ul', {'class':'mod_first_list'})

#       print qq_new
		for x in qq_new.find_all('li'):


			m_item = MusicItem()

			a = x.find('a',{'class':'mod_poster_130'})

			url = 'http://y.qq.com' + a.get('href')
			print 'song_url', 'http://y.qq.com' + a.get('href')
			em = x.find('strong', {'class':'album_name'})
			song =   em.contents[0]
			print 'song', em.contents[0].encode('utf8')
			em = x.find('strong', {'class':'album_singer'})
			singer =  em.contents[0]
			print 'singer', em.contents[0].encode('utf8')



			m_item['song'] = song
			m_item['url'] = url
			m_item['singer'] = singer
			m_item['source'] = u'QQ'
			now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			m_item['date'] = now
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
		print 'song_url' , 'http://www.xiami.com' +p[0].find('a').get('href')
		print 'song', p[0].find('a').string.encode('utf8')
		print 'singer', p[1].find('a').string.encode('utf8')	
		m_item = MusicItem()
		m_item['song'] = song
		m_item['url'] = url
		m_item['singer'] = singer
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		m_item['date'] = now
		items.append(m_item)


		for sibling in info.next_siblings:
                #print(repr(sibling))
                #break
			if(sibling !=' ' ):
				a = sibling.find('div',{'class':'info'})
				p = a.find_all('p')
                        #print p
				print 'song_url' , 'http://www.xiami.com' + p[0].find('a').get('href')
				print 'song', p[0].find('a').string.encode('utf8')
				print 'singer', p[1].find('a').string.encode('utf8')


				url = 'http://www.xiami.com' +p[0].find('a').get('href')
				song =  p[0].find('a').string
				singer =  p[1].find('a').string
				source = 'xiami'
				print 'song_url' , 'http://www.xiami.com' +p[0].find('a').get('href')
				print 'song', p[0].find('a').string.encode('utf8')
				print 'singer', p[1].find('a').string.encode('utf8')


				m_item = MusicItem()
				m_item['song'] = song
				m_item['url'] = url
				m_item['singer'] = singer
				m_item['source'] = source
				now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

				m_item['date'] = now
				items.append(m_item)


		return items

	def parse163(self, response):

		soup = BeautifulSoup(response.body)
        #print text
		a       = soup.find('div', {'class':'roll f-pr'})
        #print a
		items = []
		for x in a.find_all('li'):

			p = x.find_all('p')


			url = 'http://music.163.com/#' +p[0].find('a').get('href')
			song =  p[0].find('a').string
			singer =  p[1].find('a').string
			source = '163'
			print 'song_url' , 'http://music.163.com/#' +p[0].find('a').get('href')
			print 'song', p[0].find('a').string.encode('utf8')
			print 'singer', p[1].find('a').string.encode('utf8')


			m_item = MusicItem()
			m_item['song'] = song
			m_item['url'] = url
			m_item['singer'] = singer
			now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			m_item['source'] = source
			m_item['date'] = now
			items.append(m_item)

		return items




		#sel = Selector(response)
		#sites = sel.xpath('//td[@class="title"]')
		#for site in sites:
	#	title = site.xpath('a/text()').extract()
	#	link = site.xpath('a/@href').extract()
  

		#print title, link



