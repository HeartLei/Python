# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from Maoyan.items import MaoyanItem

class MaoyanvideosSpider(scrapy.Spider):
    name = "maoyanVideos"
    allowed_domains = ["maoyan.com"]
    start_urls = 'http://maoyan.com/board/4/'

    # 请求首页
    def start_requests(self):
        yield Request(url=self.start_urls, callback=self.parse)

    # 组装url
    def parse(self, response):
        for i in range(0,10):
            url = self.start_urls + "?offset=" + str(i*10)
            yield Request(url=url, callback=self.parse_page)

    # 解析页面
    def parse_page(self, response):
        item = MaoyanItem()
        reg = re.compile(
            '<img data-src="http://p0.meituan.net/movie/(.*?)" .*?/>.*?<a href=".*?".*?>(.*?)</a>.*?<p class=".*?">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?<i class="integer">(.*?)</i><i class="fraction">(.*?)</i>',
           re.S)
        contes = reg.findall(response.text)
        for cont in contes:
            item['img_url']='http://p0.meituan.net/movie/'+ cont[0],
            item['title']=cont[1],
            item['star_name']=cont[2].strip(),
            item['show_time']=cont[3],
            item['score']=cont[4] + cont[5]
        return item
