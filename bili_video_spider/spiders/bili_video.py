# -*- coding: utf-8 -*-
import datetime
import json
import time

from scrapy.http import Request
import scrapy
from ..utils import begin_aid as beginaid, end_aid as endaid, sub_channel_2_channel, params_count
from ..items import BiliVideoSpiderItem

class BiliVideoSpider(scrapy.Spider):

    name = 'bili_video'  #爬虫的名字，一定要写且唯一
    allowed_domains = ['bilibili.com']  #允许的域，非bilibili.com域名的连接都不爬取
    start_urls = []   #第一个爬取的url
    custom_settings = {
        'ITEM_PIPELINES': {
            'bili_video_spider.pipelines.BiliVideoSpiderPipeline': 300
        }
    }
    #用来记录目前解析了多少条数据
    count = 0
    #用来记录什么时候开始爬虫
    begin_time = time.time()
    def start_requests(self):

        #爬取视频信息的url
        url = 'https://api.bilibili.com/x/article/archives?ids='

        #第一个爬取的av号
        begin_aid = beginaid

        #最后一个爬取的av号
        end_aid = endaid

        #i用来记录拼接的参数,100个av号后发送一次请求
        i = 0

        #url的参数
        params = ''

        #记录爬取了多少条
        count_sum = 0

        #直到开始的av号比最后的av号大，退出循环
        while begin_aid <= end_aid:

            #拼接参数
            params += str(begin_aid) + ','

            #拼接一个参数i就加一
            i += 1

            #判断是否拼接了100个参数或者已经到最后一个参数
            if i == params_count or begin_aid == end_aid:

                #记录爬取了多少条
                count_sum += i

                #把计数的i改为0重新计数
                i = 0

                # print("*****************************【爬虫已用时----[{}  s]】*****************************"
                #       .format(time.time() - begin_time))
                print("*****************************【已爬取了[ {} ]条数据，共用时 [ {} s]】*****************************"
                      .format(count_sum, time.time() - self.begin_time))

                #发送请求，并返回给parse函数处理
                yield Request(url+params.rstrip(','))
                #处理完成请求后把参数清空

                params = ''

            #每循环一遍aid就加一
            begin_aid += 1



    def parse(self, response):
        try:
            #用json加载响应体
            res = json.loads(response.body)

            #获取data数据
            data = res['data']

            #获取此次请求成功的av号，存入key_list列表
            key_list = list(data.keys())
            #记录存储的多少条数据

            #遍历请求成功的视频的数据
            for key in key_list:
                self.count += 1
                #把数据存储到items中
                subTagName = data[key]['tname']
                item = BiliVideoSpiderItem()
                item['aid'] = data[key]['aid']
                item['title'] = data[key]['title']
                item['pic'] = data[key]['pic']
                item['subTagName'] = subTagName
                item['pubdate'] = data[key]['pubdate']
                item['mid'] = data[key]['owner']['mid']
                item['name'] = data[key]['owner']['name']
                item['cur_view'] = data[key]['stat']['view']
                item['cur_danmuku'] = data[key]['stat']['danmaku']
                item['cur_reply'] = data[key]['stat']['reply']
                item['cur_favorite'] = data[key]['stat']['favorite']
                item['cur_coin'] = data[key]['stat']['coin']
                item['cur_share'] = data[key]['stat']['share']
                item['cur_like'] = data[key]['stat']['like']
                item['cur_date'] = datetime.datetime.now()
                item['cur_count'] = self.count

                #判断子分区存不存在，若存在则取到大分区的值赋给items
                if subTagName != '':
                    tagName = sub_channel_2_channel[subTagName]
                    item['tagName'] = tagName
                #因为有3个分区都有【资讯】子分区，所以要单独处理
                elif subTagName == '资讯':
                    if data[key]['tid'] == 170:
                        item['tagName'] == '国创'
                    if data[key]['tid'] == 51:
                        item['tagName'] = '番剧'
                    if data[key]['tid'] == 159:
                        item['tagName'] = '娱乐'
                else:
                    item['tagName'] = ''

                #item赋完值就返回给管道进一步处理
                yield item

        except Exception as e:
            if data['code'] == -404:
                print("【请求页面404】")
                return
            print("【解析数据异常】信息------>{}".format(e))
