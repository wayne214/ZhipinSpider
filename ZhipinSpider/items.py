# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhipinspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 工作名称
    title = scrapy.Field()
    # 工资
    salary = scrapy.Field()
    # 公司
    company = scrapy.Field()
    # 工作详细链接
    url = scrapy.Field()
    # 工作地址
    work_addr = scrapy.Field()
    # 行业
    industry = scrapy.Field()
    # 公司规模
    company_size = scrapy.Field()
    # 招聘者
    recruiter = scrapy.Field()
    # 发布时间
    publish_date = scrapy.Field()
