# -*- coding: utf-8 -*-
import logging
import time
from datetime import datetime

import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class BiliVideoSpiderPipeline(object):
    def __init__(self):
        #初始化时连接数据库
        self.con = pymysql.connect(host='localhost',
                                   user='root',
                                   password='123456',
                                   database='bili',
                                   charset='utf8')
        #创建数据库游标
        self.cursor = self.con.cursor()
        self.time = time.time()


    def process_item(self, item, spider):
        try:
            #插入数据sql语句
            sql = '''
                        insert into bili_video (video_id,author_id,video_title,video_pic,channel,subchannel,author,pub_date,
                                                cur_view,cur_favorite,cur_danmuku,cur_coin,cur_share,cur_like,cur_datetime)
                              value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    '''
            #插入sql的字段参数
            params_item = [item['aid'], item['mid'], item['title'], item['pic'], item['tagName'], item['subTagName'],
                           item['name'], datetime.fromtimestamp(item['pubdate']), item['cur_view'], item['cur_favorite'],
                           item['cur_danmuku'], item['cur_coin'], item['cur_share'], item['cur_like'], item['cur_date']]
            #执行sql语句
            self.cursor.execute(sql, params_item)
            #提交
            self.con.commit()
            print("-----------------------------【已解析[ {} ]条数据,用时[ {} ]当前av号[ {} ]】-----------------------------"
                  .format(item['cur_count'], time.time() - self.time, item['aid']))
        except Exception as e:
            print("执行sql插入操作异常，信息------>{}".format(e))

        return item

    def close_spider(self, spider):
        #爬虫关闭时关闭sql连接
        self.cursor.close()
        self.con.close()


class BiliVideoRankOneSpiderPipelines(object):
    def __init__(self, my_setting):
        self.my_setting = my_setting
        self.con = pymysql.connect(host='localhost',
                                   user='root',
                                   password='123456',
                                   database='bili',
                                   charset='utf8')
        self.cursor = self.con.cursor()
        self.time = time.time()

    #重写from_crawler方法，作用于获取settings的参数
    @classmethod
    def from_crawler(cls, crawler):
        my_setting = crawler.settings
        return cls(my_setting)

    def process_item(self, item, spider):
        sql = ''
        if item['spider_day'] == 1: #爬1日的排名
            sql = '''
                insert into bili_video_rank_1(aid,title,author,mid,coins,play,video_review,
                duration,pic,cid,pts,cur_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        elif item['spider_day'] == 7: #爬7日的排名
            sql = '''
                insert into bili_video_rank_7(aid,title,author,mid,coins,play,video_review,
                duration,pic,cid,pts,cur_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        elif item['spider_day'] == 30: #爬30日的排名
            sql = '''
                insert into bili_video_rank_30(aid,title,author,mid,coins,play,video_review,
                duration,pic,cid,pts,cur_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        params = [
            item['aid'], item['title'], item['author'], item['mid'], item['coins'], item['play'], item['video_review'],
            item['duration'], item['pic'], item['cid'], item['pts'], item['cur_date']
        ]
        try:
            self.cursor.execute(sql, params)
            self.con.commit()
            print("【使用的USER-AGENT是--->[ {} ]】".format(self.my_setting.get('USER_AGENT')))
            print("-----------------------【已解析[ {} ]条数据,用时[ {} ]当前av号[ {} ]】-----------------------"
                  .format(item['cur_count'], time.time() - self.time, item['aid']))
        except Exception as e:
            logging.error("执行sql插入操作异常，信息------>{}".format(e))

        return item

    def close_spider(self, spider):
        # 爬虫关闭时关闭sql连接
        self.cursor.close()
        self.con.close()


class BiliUpSpiderPinelines(object):

    def __init__(self):
        self.con = pymysql.connect(host='localhost',
                              user='root',
                              password='123456',
                              database='bili',
                              charset='utf8')
        self.cursor = self.con.cursor()

    def process_item(self, item, spider):
        sql = '''
            insert into bili_up_info(mid,name,sex,level,follower,following,
                videos,article,album,audio,archive_total,article_total,official,cur_date)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        params = [
            item['mid'], item['name'], item['sex'], item['level'],
            item['follower'], item['following'], item['videos'],
            item['article'], item['album'], item['audio'],
            item['archive_total'], item['article_total'], item['official'], item['cur_date']
        ]
        try:
            self.cursor.execute(sql, params)
            self.con.commit()
            print('---------------【爬取第[ {} ]个up主[ {} ]，uid[ {} ]成功！】---------------'
                  .format(item['i']+1, item['name'], item['mid']))
        except Exception as e:
           logging.error("执行sql插入操作异常，信息------>{}".format(e))

    def close_spider(self, spider):
        print("【[ {} ] 完成爬虫!!】".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        self.cursor.close()
        self.con.close()
