from scrapy import cmdline
name = 'bili_up_info'
cmdline.execute('scrapy crawl {}'.format(name).split())