# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Rule
from ZhipinSpider.items import ZhipinspiderItem
from scrapy.linkextractors import LinkExtractor
import time


class JobPositionSpider(scrapy.Spider):
    # 定义该Spider的名字
    name = 'job_position'
    # 允许爬取的域名
    allowed_domains = ['zhipin.com']

    # 爬取的首页列表
    start_urls = ['https://www.zhipin.com/c101280100/h_101280100/']

    cookies = {
        '_uab_collina=157648562499015413993343; __c=1576485624; __g=-; __l=l=%2Fwww.zhipin.com%2Fweb%2Fcommon%2Fsecurity-check.html%3Fseed%3D%252BbshLH7E%252Bmx1ulQG2KuimpnTevHPc5FG19ZasWTLm0U%253D%26name%3D6c486237%26ts%3D1576485623273%26callbackUrl%3D%252Fc101280100%252Fh_101280100%252F%26srcReferer%3D&r=&friend_source=0&friend_source=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1576485625; __a=5610085.1576485624..1576485624.19.1.19.19; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1576575674; __zp_stoken__=cfffnKJXmyi0G8KKLMgyJlNc8M4Td9jogpAYou2hKoQSCqXX%2BRlmbzmrStJLdcUZCFFfBzuslwI4Ov4rn8FJfLt%2FpNahALSloS7Ff%2BolRnyVwsfE7phONMVSoHAXjH%2B2h9qD'
    }

    # 发送 header，伪装为浏览器
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': cookies,
            'Host': 'www.zhipin.com',
            'Origin': 'https://www.zhipin.com',
            'Referer': 'https://www.zhipin.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }
    }

    # 该方法负责提取response所包含的信息
    # response代表下载器从start_urls中每个URL下载得到的响应
    def parse(self, response):

        new_links = response.xpath('//div[@class="page"]/a[@class="next"]/@href').extract()
        if new_links and len(new_links) > 0:
            # 获取下一页的链接
            new_link = new_links[0]
            # 再次发送请求获取下一页数据
            yield scrapy.Request("https://www.zhipin.com" + new_link, callback=self.parse)

        # print('---***--response {} -{}-'.format(response, response.selector.xpath('//div[@class="job-list"]//li')))
        # 遍历页面上所有//div[@class="job-primary"]节点

        item = ZhipinspiderItem()
        for job_primary in response.xpath('//div[@class="job-primary"]'):

            print('---***--job_primary {} --'.format(job_primary))

            # 匹配//div[@class="job-primary"]节点下/div[@class="info-primary"]节点
            # 也就是匹配到包含工作信息的<div.../>元素
            info_primary = job_primary.xpath('./div[@class="info-primary"]')
            item['title'] = info_primary.xpath('./h3/a/div[@class="job-title"]/text()').extract_first()
            item['salary'] = info_primary.xpath('./h3/a/span[@class="red"]/text()').extract_first()
            item['work_addr'] = info_primary.xpath('./p/text()').extract_first()
            item['url'] = info_primary.xpath('./h3/a/@href').extract_first()
            # 匹配//div[@class="job-primary"]节点下./div[@class="info-company"]节点下
            # 的/div[@class="company-text"]的节点
            # 也就是匹配到包含公司信息的<div.../>元素
            company_text = job_primary.xpath('./div[@class="info-company"]' +
                                             '/div[@class="company-text"]')
            item['company'] = company_text.xpath('./h3/a/text()').extract_first()
            company_info = company_text.xpath('./p/text()').extract()
            if company_info and len(company_info) > 0:
                item['industry'] = company_info[0]
            if company_info and len(company_info) > 2:
                item['company_size'] = company_info[2]
            # 匹配//div[@class="job-primary"]节点下./div[@class="info-publis"]节点下
            # 也就是匹配到包含发布人信息的<div.../>元素
            info_publis = job_primary.xpath('./div[@class="info-publis"]')
            item['recruiter'] = info_publis.xpath('./h3/text()').extract_first()
            item['publish_date'] = info_publis.xpath('./p/text()').extract_first()

            yield item

