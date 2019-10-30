# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime

import scrapy
from scrapy.http import Request
import logging
from ..items import BiliVideoRankOneSpiderItem


class BiliVideoRank1Spider(scrapy.Spider):
    name = 'bili_video_rank'
    allowed_domains = ['bilibili.com']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'bili_video_spider.pipelines.BiliVideoRankOneSpiderPipelines': 300
        }
    }

    #params用来接收命令行参数，命令行用【-a】来设置参数，格式：NAME=VALUE
    def __init__(self, params, *args, **kwargs):
        super(BiliVideoRank1Spider, self).__init__(*args, **kwargs)
        self.params = params
        self.begin_time = time.time()



    def start_requests(self):
        url = 'https://api.bilibili.com/x/web-interface/ranking?rid={}&day={}&type={}&arc_type={}'

        #切割参数
        param = str(self.params).split(',')

        #取参数，并转换成int类型
        _rid = int(param[0])
        _day = int(param[1])
        _type = int(param[2])
        _arc_type = int(param[3])

        print("*****************************【开始发送请求，共用时 [ {} s]】*****************************"
              .format(time.time() - self.begin_time))
        #发送请求
        yield Request(url=url.format(_rid, _day, _type, _arc_type))

    #解析数据
    def parse(self, response):
        # print('【USER_AGENT------------------>[ '+str(response.headers)+' ]】')
        try:
            res = json.loads(response.body)
            data_list = res['data']['list']
            cur_date = datetime.now()
            cur_count = 0
            for data in data_list:
                cur_count += 1
                item = BiliVideoRankOneSpiderItem()
                item['aid'] = data['aid']
                item['author'] = data['author']
                item['coins'] = data['coins']
                item['duration'] = data['duration']
                item['mid'] = data['mid']
                item['pic'] = data['pic']
                item['cid'] = data['cid']
                item['play'] = data['play']
                item['pts'] = data['pts']
                item['title'] = data['title']
                item['video_review'] = data['video_review']
                item['cur_date'] = cur_date
                item['spider_day'] = int(str(self.params).split(',')[1])
                item['cur_count'] = cur_count
                yield item
                if 'others' in data:
                    for others in data['others']:
                        cur_count += 1
                        item['aid'] = others['aid']
                        item['author'] = data['author']
                        item['coins'] = others['coins']
                        item['duration'] = others['duration']
                        item['mid'] = data['mid']
                        item['pic'] = others['pic']
                        item['play'] = others['play']
                        item['pts'] = others['pts']
                        item['title'] = others['title']
                        item['video_review'] = others['video_review']
                        item['cid'] = 0
                        item['cur_date'] = cur_date
                        item['spider_day'] = int(str(self.params).split(',')[1])
                        item['cur_count'] = cur_count
                        yield item
        except Exception as e:
            if data['code'] == -404:
                logging.error('【页面404】')
                return
            logging.error("【解析数据异常】信息------>{}".format(e))


