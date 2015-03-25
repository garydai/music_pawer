# -*- coding: utf-8 -*-

# Scrapy settings for m_p project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'm_p'

SPIDER_MODULES = ['m_p.spiders']
NEWSPIDER_MODULE = 'm_p.spiders'

ITEM_PIPELINES = {'m_p.pipelines.mysql_pipeline':2, 'm_p.pipelines.download_image_pipeline':1 }

SERVER = "localhost"
PORT = 3306
DB = "music"
COLLECTION = "music"
USER = 'root'
PASSWORD = ''
CHARSET = 'utf8'
IMAGES_STORE='/home/admin/nginx/html/yii/demos/music_web/images/cover/'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'm_p (+http://www.yourdomain.com)'
