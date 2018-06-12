# -*- coding: utf-8 -*-

import scrapy
import requests
import re
import html
from scrapySpider01.spiders.getSomething import getUrls
from scrapySpider01.items import Scrapyspider01Item
import json
from scrapySpider01.items import Scrapyspider01Item

class spider00(scrapy.Spider):
    name = 'td_spider'
    allowed_domains = ["www.toutiao.com"]
    start_urls = getUrls(page=1, keyWord='头条')


    def parse(self, response):
        absText = response.body
        absDic = json.loads(absText)
        datas = absDic['data']
        for data in datas:
            if('group_id' in data.keys()):
                mainUrl = 'https://www.toutiao.com/a'+str(data['group_id'])+'/'
                yield self.sec_parse(mainUrl)

    def sec_parse(self, url):
        fullText = requests.get(url=url).text
        item = Scrapyspider01Item()
        try:
            reTitle = '<title>.*?</title>'
            reg = re.compile(reTitle)
            title = reg.findall(fullText)
            item['title'] = str(title[0][7:-8])
            #self.log('文章标题：' + str(item['title']))

            reContent = 'content: \'&lt;div&gt;&lt;.*?&lt;/div&gt;\''
            reg = re.compile(reContent)
            content = reg.findall(fullText)
            if content != "" and content != None:
                content = html.unescape(content[0][10:-1])
                reg = re.compile('<p>.*?<').findall(content)
                res = ""
                for i in reg:
                    i = i[3:-1]
                    if i[0:1] != '<':
                        res += i + ' '
                item['main_body'] = str(res)
                item['abstract'] = str(reg[0][3:-1])

            item['originUrl'] = str(url)

            self.log("文章："+item['title']+" 爬取成功")

            return item

        except:
            self.log('文章' + item['title']+" 爬取失败, 可能没有文本信息")



