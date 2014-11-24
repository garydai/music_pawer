# coding=utf-8
import HTMLParser
from bs4 import BeautifulSoup
import urllib
import urllib2
import socket 
import sys
'''
# timeout in seconds 
timeout = 50 
socket.setdefaulttimeout(timeout) 
'''
'''
class parseLinks(HTMLParser.HTMLParser):
	def handle_starttag(self, tag, attrs):
		if tag == 'em':
			for name,value in attrs:
				if name == 'id':
					print value
lParser = parseLinks()
lParser.feed(urllib.urlopen("http://y.qq.com/y/static/index.html").read())
'''
'''	
	text = html.read(90000)
	html.close()
'''
f = open("new_song_list.txt","wb+")
f2 = open("random_song_list.txt","wb+")
try:

	##qqmusic
	html = urllib.urlopen('http://y.qq.com/y/static/index.html')
	tt = ''
	for i in range(0, 9):
		text = html.read(10000)
		tt += text

	soup = BeautifulSoup(tt)

	qq_new	= soup.find('ul', {'class':'mod_first_list'})
	
	for x in qq_new.find_all('li'):	
		a = x.find('a',{'class':'mod_poster_130'})	
		print 'song_url', 'http://y.qq.com' + a.get('href')	
		em = x.find('strong', {'class':'album_name'})
		print 'song', em.contents[0].encode('utf8')
		em = x.find('strong', {'class':'album_singer'})
		print 'singer', em.contents[0].encode('utf8')


	#xiami 
	url = 'http://www.xiami.com'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	values = {'name' : 'Michael Foord',
    	      'location' : 'Northampton',
        	  'language' : 'Python' }
	headers = { 'User-Agent' : user_agent }
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	the_page = response.read()	

	soup = BeautifulSoup(the_page)

	xiami_new	= soup.find('div', {'id':'albums'})
	info = xiami_new.find('div',{'class':'album'})				
	#print info
	a = info.find('div',{'class':'info'})	
	p = a.find_all('p')	

	print 'song_url' , 'http://www.xiami.com' +p[0].find('a').get('href')
	print 'song', p[0].find('a').string.encode('utf8')
	print 'singer', p[1].find('a').string.encode('utf8')
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
		#print a
	#for x in xiami_new:	
	#	a = x.find('div',{'class':'info'})								
	#	info = a.find_all('p')
	#	print info[0].contents

except socket.error, msg:
	print 'error'
    