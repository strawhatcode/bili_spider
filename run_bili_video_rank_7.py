from scrapy import cmdline
cammand = 'scrapy crawl bili_video_rank -a params=0,7,1,0'
cmdline.execute(cammand.split())