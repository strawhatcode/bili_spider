# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime

import scrapy
from scrapy.http import Request

import pymysql

from ..items import BiliUpInfoSpiderItem

# 爬取up主信息
class BiliUpInfoSpider(scrapy.Spider):
    name = 'bili_up_info'
    allowed_domains = ['bilibili.com']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'bili_video_spider.pipelines.BiliUpSpiderPinelines': 300   #设置管道
        }
    }

    # 开始发送请求
    def start_requests(self):
        print("【[ {} ] up主信息爬虫开始】".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        url = 'https://api.bilibili.com/x/space/acc/info?mid='
        con = pymysql.connect(host='localhost',
                              user='root',
                              password='123456',
                              database='bili',
                              charset='utf8')
        cursor = con.cursor()
        sql = '''
                select up_uid from upuid where id < 5
              '''
        cursor.execute(sql)
        result = cursor.fetchall()  # 查询upuid表中的所有uid
        cursor.close()
        con.close()
        uids = []
        for i in range(len(result)):
            uids.append(str(result[i][0]))  # 把查询的结果存到uids列表中
        # uids = ['391679']
        for i, uid in enumerate(uids):
            # print('【开始发送第一个请求】')
            yield Request(url + str(uid), meta={'i': i})

    # 解析第一个请求
    def parse(self, response):
        res = json.loads(response.body)
        data = res['data']
        # print(data)
        # uid = response.meta['uid']  #获取到元数据
        item = BiliUpInfoSpiderItem()  # 实例化item
        item['i'] = response.meta['i'] #记录爬取了第几个up
        item['mid'] = data['mid']
        item['name'] = data['name']
        item['sex'] = data['sex']
        item['level'] = data['level']
        item['official'] = data['official']['title']
        # item['vip_type'] = data['vip']['type']
        # item['vip_status'] = data['vip']['status']
        # print("【开始发送第二个请求】")
        yield Request('https://api.bilibili.com/x/relation/stat?vmid=' + str(item['mid']),  # 发送第二个请求
                      meta={'item': item},   # 把item作为元数据传递给下个解析函数
                      callback=self.parse_following)  # 指定自定义的解析函数来解析这个请求

    # 自定义解析函数，用来解析up主粉丝的url
    def parse_following(self, response):
        res = json.loads(response.body)
        data = res['data']
        # print(data)
        item = response.meta['item']  # 获取到请求传过来的元数据
        item['following'] = data['following']
        item['follower'] = data['follower']
        # print("【开始发送第三个请求】  ")
        yield Request('https://api.bilibili.com/x/space/navnum?mid=' + str(item['mid']),
                      meta={'item': item},
                      callback=self.parse_vaaa)
        # yield Request('https://elec.bilibili.com/api/query.rank.do?mid=' + str(item['mid']),
        #               meta={'item': item},
        #               callback=self.parse_flash)

    # 解析up主充电人数的url
    # def parse_flash(self, response):
    #     res = json.loads(response.body)
    #     data = res['data']
    #     # print(data)
    #     item = response.meta['item']
    #     item['flash_count'] = data['count']
    #     item['flash_total_count'] = data['total_count']
    #     yield Request('https://api.bilibili.com/x/space/navnum?mid=' + str(item['mid']),
    #                   meta={'item': item},
    #                   callback=self.parse_vaaa)
    #     # print('解析完成！！！！！！！！！！！！！')

    # 解析up主视频、文章、相簿和音频url， v:video, a:article, a:album, a:audio
    def parse_vaaa(self, response):
        res = json.loads(response.body)
        data = res['data']
        # print(data)
        item = response.meta['item']
        item['videos'] = data['video']
        # item['bangumi'] = data['bangumi']
        # item['channel'] = data['channel']['master']
        # item['favourite'] = data['favourite']['master']
        item['article'] = data['article']
        item['album'] = data['album']
        item['audio'] = data['audio']
        # print("【开始发送第四个请求】")
        yield Request('https://api.bilibili.com/x/space/upstat?mid=' + str(item['mid']),
                      meta={'item': item},
                      callback=self.parse_video_and_article_view)

    # 解析视频和文章的总播放量或点击量
    def parse_video_and_article_view(self, response):
        res = json.loads(response.body)
        data = res['data']
        # print(data)
        item = response.meta['item']
        item['archive_total'] = data['archive']['view']
        item['article_total'] = data['article']['view']
        item['cur_date'] = datetime.now()
        # print("【解析完成！！！！！！！！！！！！！！！！！！！！】")
        yield item