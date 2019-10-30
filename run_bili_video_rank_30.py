from scrapy import cmdline
cammand = 'scrapy crawl bili_video_rank -a params=0,30,1,0'
cmdline.execute(cammand.split())