# -*- coding: utf-8 -*-
from scrapySpider01 import settings
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Scrapyspider01Pipeline(object):

    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.db = 'toutiao01'


    def process_item(self, item, spider):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user='root', password='admin', db=self.db,
                                        use_unicode=True, charset='utf8')
            self.cur = self.conn.cursor()

            if(self.noRepetition(item['title'])):
                sql = 'insert into toutiao(title, abstract, main_body, originUrl, comments)  values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' \
                      %(item['title'], item['abstract'], item['main_body'], item['originUrl'], item['comments'])
                self.cur.execute(sql)
                self.conn.commit()
                print("文章: "+item['title']+"储存成功")
            else:
                print("文章："+item['title']+"已存在数据库中")
        except:
            self.conn.rollback()
            print("文章:"+item['title']+"储存失败")
        self.cur.close()
        self.conn.close()

    def noRepetition(self, title):
        sql = 'select * from toutiao where title=\'%s\';' %(title)
        res = self.cur.execute(sql)
        if res == 0:
            return True
        else:
            return False
