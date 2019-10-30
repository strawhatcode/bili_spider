from scrapy import cmdline
command = 'scrapy crawl bili_video_rank -a params=0,1,1,0'
cmdline.execute(command.split())