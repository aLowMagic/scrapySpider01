# -*- coding: utf-8 -*-

import scrapy
import requests
import re
import html
from scrapySpider01.spiders.getSomething import getUrls
import json
from scrapySpider01.items import Scrapyspider01Item

class spider00(scrapy.Spider):
    name = 'td_spider'
    allowed_domains = ["www.toutiao.com"]
    start_urls = getUrls(page=1, keyWord='dota2')


    def parse(self, response):
        absText = response.body
        absDic = json.loads(absText)
        datas = absDic['data']
        for data in datas:
            if('group_id' in data.keys()):
                mainUrl = 'https://www.toutiao.com/a'+str(data['group_id'])+'/'
                yield self.sec_parse(data['group_id'], mainUrl)

    def sec_parse(self, group_id, url):
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
            item['comments'] = self.getComments(group_id)

            self.log("文章："+item['title']+" 访问成功")

            return item

        except:
            self.log('文章' + item['title']+" 爬取失败, 可能没有文本信息")



    def getComments(self, group_id):
        url = 'https://www.toutiao.com/api/comment/list/?group_id=%s&item_id=%s&offset=0&count=20' %(group_id, group_id)
        commentsRequest = requests.get(url=url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                                                         ' Chrome/67.0.3396.87 Safari/537.36'})
        text = json.loads(commentsRequest.text)
        comments = (text['data'])

        total = comments['total']
        comments = comments['comments']
        res = []
        res.append({'total': str(total)})
        if int(total) > 0:
            for com in comments:
                name = com['user']['name']
                text = com['text']
                res.append({name: text})
        comm = json.dumps(res, ensure_ascii=False)
        return comm