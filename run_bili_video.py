from scrapy import cmdline
name = 'bili_video'
#启动spider的python
cmdline.execute('scrapy crawl {}'.format(name).split())