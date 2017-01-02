# -*- coding: utf-8 -*-
import scrapy,json
from ximalaya.settings import START_URL,BASE_URL
from scrapy.selector import Selector
from ximalaya.items import XimalayaItem
class FmspiderSpider(scrapy.Spider):
    name = "fmspider"
    allowed_domains = ["www.ximalaya.com","audio.xmcdn.com"]
    start_urls = [START_URL]

    def parse(self, response):
        sel = Selector(response)
        for url in sel.xpath('//*[@id="mainbox"]/div/div[1]/div/div[2]/div[5]/div/a/@href')\
                .extract():
            request = scrapy.Request(BASE_URL+url,callback=self.parse)
            yield request

        for url in sel.xpath('//*[@id="mainbox"]/div/div[1]/div/div[2]/div[4]/ul/li/@sound_id')\
                .extract():
            name = sel.xpath('//*[@id="mainbox"]/div/div[1]/div/div[2]/div[1]/div[1]/d'
                             'iv[2]/div[1]/h1/text()').extract()[0]
            request = scrapy.Request('http://www.ximalaya.com/tracks/'+url+'.json',
                                     callback=self.parse_item,meta={'name':name})
            yield request


    def parse_item(self,response):
        item = XimalayaItem()
        data = json.loads(response.body_as_unicode())
        item['name'] = response.meta['name']
        item['play_path'] = data['play_path']
        item['title'] = data['title']
        return item



