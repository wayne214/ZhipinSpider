# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
import mysql.connector


class ZhipinspiderPipeline(object):
    def process_item(self, item, spider):
        print("工作:", item['title'])
        print("工资:", item['salary'])
        print("工作地点:", item['work_addr'])
        print("详情链接:", item['url'])
        print("公司:", item['company'])
        print("行业:", item['industry'])
        print("公司规模:", item['company_size'])
        print("招聘人:", item['recruiter'])
        print("发布日期:", item['publish_date'])
        return item


class ImportToJson(object):
    # 创建json文件
    def __init__(self):
        # 构建json文件的名称，bosszhipin_日期.json
        jsonName = 'bosszhipin_' + str(time.strftime("%Y%m%d", time.localtime())) + '.json'
        self.f = open(jsonName, 'w')

    # 打开爬虫时执行的动作
    def open_spider(self, spider):
        pass

    # 主管道
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(content)
        return item

    # 爬虫关闭时执行的动作
    def close_spider(self, spider):
        self.f.close()


class ImportToMysql(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password="12345678", host='localhost', port="3306", database='runoob', use_unicode=True)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        print('--------关闭数据库资源------')
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute("INSERT INTO job_inf VALUES(null, %s, %s, %s, %s, %s, \
                    %s, %s, %s, %s)", (item['title'], item['salary'], item['company'],
                                       item['url'], item['work_addr'], item['industry'],
                                       item.get('company_size'), item['recruiter'], item['publish_date']))
        self.conn.commit()
