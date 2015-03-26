# coding=utf-8
import HTMLParser
from bs4 import BeautifulSoup
import urllib
import urllib2
import socket 
import sys
import dbconfig
import MySQLdb as mdb
from datetime import *
import json
import requests

try:

	conn = dbconfig.connectDB()
	cur  = conn.cursor(mdb.cursors.DictCursor)
	


	#xiami 

	now = datetime.now().strftime('%Y-%m-%d 00:00:00')

        sql = 'select * from music where source="xiami" and date > "%s"' %now

        cur.execute(sql)
        results = cur.fetchall()

	for item in results:



		page = 1
		while 1:

			url = 'http://www.xiami.com/commentlist/turnpage/id/'+ item['album_id']+'/page/' + str(page) + '/ajax/1?type=1'

			user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
			values = {'name' : 'Michael Foord',
    			      'location' : 'Northampton',
        			  'language' : 'Python' }
			headers = { 'User-Agent' : user_agent }
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data, headers)
			response = urllib2.urlopen(req)
			the_page = response.read()	

			soup  = BeautifulSoup(the_page)
			div = soup.findAll('div', {'class':'brief'})
			for d in div:
				if d.find('div').string != None:
				
					comment = d.find('div').string
					tag = d.find('div').get('id')



					sql = 'select count(*) from other_comment where tag = "%s" ' % (tag)

					cur.execute(sql)
					results = cur.fetchone()
					if results['count(*)'] == 0:

						sql = 'insert into other_comment (album_id, comment, tag) values ("%s", "%s", "%s")' %(item['id'], comment, tag)
						cur.execute(sql)
						conn.commit()




			if the_page.find('下一页') != -1:
				page += 1
			else:
				break



	sql = 'select * from music where source="163" and date > "%s"' %now

	cur.execute(sql)
	results = cur.fetchall()

	for item in results:



                offset = 0
		limit = 20
                while 1:


			url = 'http://music.163.com/api/v1/resource/comments/R_AL_3_' + item['album_id'] + '/?rid=R_AL_3_' + item['album_id'] + '&offset=' + str(offset) + '&limit=' + str(limit) + '&total=true&csrf_token='
                        
			headers = {\
					'Host': 'music.163.com',\
    'Proxy-Connection': 'keep-alive',\
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36',\
    'Content-Type': 'application/x-www-form-urlencoded',\
    'Accept': '*/*',\
    'Referer': 'http://music.163.com/outchain/player?type =4&id=271002&auto=1&height=430&bg=e8e8e8',\
    'Accept-Encoding': 'gzip, deflate, sdch',\
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',\
    'Cookie': 'outlink_h=1579; NETEASE_AUTH_SOURCE=space; NETEASE_AUTH_USERNAME=junlintianxiajun; playliststatus=visible; _ntes_nuid=688eb18445fe95b48abce1e832f4199e; usertrack=ezq0alNDSewrKRvmQjcIAg==; usertrack=ezq0B1Nfqr/AlSuNBAZUAg==; _ntes_nnid=688eb18445fe95b48abce1e832f4199e,1402975311348; JSESSIONID=ebaluB3sO-eAE4LPRcmBu; vjuids=-77f0fed0d.146e06a394e.0.5b912416; __oc_uuid=241a4ea0-08ee-11e4-a950-5198ccf9d747; __utma=187553192.874452700.1405077963.1405077963.1405077963.1; __utmc=187553192; SID=3b76dd6e-cc8e-40eb-8ee2-5696a3946b74; NTES_PASSPORT=kUy84AJ07Dw160XIsu72p3LPj8GkvB3YwsAMabzzKlJN4X0xpQBOS2NhqOaChzcFmV1rfdzmfygnaBqmWQGVWJ4vXAt24J8v.t79KmvEDs2ixKSg9KuUHcm2z; P_INFO=junlintianxiajun@163.com|1410966073|1|mail163|11&15|jis&1410961280&carddav#jis&320100#10#0#0|158337&1|163&mail163&blog|junlintianxiajun@163.com; NTES_SESS=0kUdYqi_Ct0Ir7SHTsjG_gLaItbpPoH.O5Xv2N8UuPGxeMp1Rj2Grz7QiG5AQkDN8FTUCbk8CYaOjpw.QCeNSlLz0wR6A7gn0v7swKyqiFBSuVOwWTf7FolapORjoNTunwXEYbe5W.wAn6uGiucXdbODFYfZuaEfkn7N5O4TL1t0kuNArGnGXz8zk; S_INFO=1411228890|1|0&80##|junlintianxiajun; ANTICSRF=787f683fdb2f9c4e2bf618927cfa140f; vjlast=1386821502.1413912750.21; ne_analysis_trace_id=1413912750268; vinfo_n_f_l_n3=4880b71680abdf9c.1.6.1404179731747.1409297575701.1413912782388; s_n_f_l_n3=4880b71680abdf9c1409297689233; playerid=84534266; JSESSIONID-163AS=ae221221df5cedc2a8d23a73b4e2f289c3f5867453d274c2fd512d648904f5ab1074ba028f5e629495be362f964012d480035d46d3d9ae744a6812691c695c84740a908c5993fc4913cc53044d2dc4ff7ff14e2f2e6b2cf450900282ba49203c04c187afa0f4e154018a53fdac68c718062eb4f84bf4b58b7569d9d802767b12; NETEASE_WDA_UID=2688375#|#1376910246232; MUSIC_U=7895b6d4e20ff9ebdbbdba907fbfff8fc94cd28437c9a97b4f278b01752a1778547307b043ee5661b2f2eb9346b4b12231b299d667364ed3; __csrf=cd2b96ffaee5f493a903b2598467ed6e; __remember_me=true; __utma=94650624.1128035981.1386494921.1419872891.1425794159.245; __utmb=94650624.8.10.1425794159; __utmc=94650624; __utmz=94650624.1389779298.46.2.utmcsr=twebmail.mail.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/js5/main.jsp'
}

			r = requests.get(url = url,headers = headers)
#print r.text
			#print(r.text.encode('utf8'))
                        the_page = r.text
			t = json.loads(the_page.encode('utf8'))
			print item['id']
			print t['more']

			flag = 0
			for comment in t['comments']:
				print comment
				sql = 'select count(*) from other_comment where tag = "%s" ' % (str(comment['commentId']))
				
				cur.execute(sql)
				results = cur.fetchone()
				if results['count(*)'] == 0:

					sql = 'insert into other_comment (album_id, comment, tag) values ("%s", "%s", "%s")' %(item['id'], comment['content'], str(comment['commentId']))
					cur.execute(sql)
					conn.commit()
				else:
					flag = 1
					break
			if t['more'] == True and flag == 0:
				offset += limit
			else:
				break
#			print t





except Exception, e:
	print e
conn.close() 
