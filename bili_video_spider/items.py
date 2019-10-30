# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 爬取所有视频用的item
class BiliVideoSpiderItem(scrapy.Item):
    aid = scrapy.Field()  # 视频av号
    title = scrapy.Field()  # 视频标题
    mid = scrapy.Field()  # up主uid
    name = scrapy.Field()  # up主名称
    pubdate = scrapy.Field()  # 视频发布日期
    pic = scrapy.Field()   # 视频封面
    tagName = scrapy.Field()  # 视频分区
    subTagName = scrapy.Field()  # 视频子分区
    cur_view = scrapy.Field()  # 当前播放
    cur_danmuku = scrapy.Field()  # 当前弹幕数
    cur_reply = scrapy.Field()  # 当前评论
    cur_favorite = scrapy.Field()  # 当前收藏
    cur_coin = scrapy.Field()   # 当前硬币
    cur_share = scrapy.Field()  # 当前分享
    cur_like = scrapy.Field()  # 当前点赞
    cur_date = scrapy.Field()  # 当前时间
    cur_count = scrapy.Field()  # 记录解析第几条数据
    # time = scrapy.Field()   # 用来记录爬了多长时间


# 视频排名所用的item
class BiliVideoRankOneSpiderItem(scrapy.Item):
    aid = scrapy.Field()   # 视频av号
    author = scrapy.Field()  # up主名称
    cid = scrapy.Field()    # 弹幕库id
    coins = scrapy.Field()  # 硬币数
    duration = scrapy.Field()  # 视频长度
    mid = scrapy.Field()   # up主uid
    pic = scrapy.Field()  # 视频封面图片
    play = scrapy.Field()  # 播放量
    pts = scrapy.Field()   # 视频综合分数
    title = scrapy.Field()  # 视频的标题
    video_review = scrapy.Field()  # 弹幕数
    cur_date = scrapy.Field()  # 日期，用来记录哪天爬取的数据
    spider_day = scrapy.Field()  # 用来判断爬取哪个类型
    cur_count = scrapy.Field()  # 记录解析第几条数据


# up主信息item
class BiliUpInfoSpiderItem(scrapy.Item):
    i = scrapy.Field()    # 记录爬取的第几个up主
    mid = scrapy.Field()    # up主uid
    name = scrapy.Field()   # up主名字
    sex = scrapy.Field()    # up主性别
    level = scrapy.Field()  # up主等级
    official = scrapy.Field()  # up主官方头衔
    # vip_type = scrapy.Field()  # up主会员类型，2：年度大会员
    # vip_status = scrapy.Field()  # up主会员状态， 1：开通；0：没开通
    follower = scrapy.Field()  # up主粉丝数
    following = scrapy.Field()  # up主关注数
    # flash_count = scrapy.Field()  # up主本月充电人数
    # flash_total_count = scrapy.Field()  # up主总充电人数
    videos = scrapy.Field()  # up主投稿视频总数
    # bangumi = scrapy.Field()  # up主订阅番剧数
    # channel = scrapy.Field()  # up主创建的频道数
    # favourite = scrapy.Field()  # up主收藏夹总数
    article = scrapy.Field()  # up主投稿文章总数
    album = scrapy.Field()  # up主投稿相簿总数
    audio = scrapy.Field()  # up主投稿音频数
    archive_total = scrapy.Field()  # 视频总播放量
    article_total = scrapy.Field()  # 文章总点击量
    cur_date = scrapy.Field()  # 用来记录爬虫的时间
