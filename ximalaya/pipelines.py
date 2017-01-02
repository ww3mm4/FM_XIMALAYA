# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from io import BytesIO
from scrapy.contrib.pipeline.files import FilesPipeline
import scrapy
from scrapy.exceptions import DropItem
from scrapy.utils.misc import md5sum


class XimalayaPipeline(FilesPipeline):

    def file_downloaded(self, response, request, info):
        path = self.file_custom_key(response)
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        buf.seek(0)
        self.store.persist_file(path, buf, info)
        return checksum

    def file_custom_key(self, response):
        title = response.meta['title']
        name = response.meta['name']
        file_key = name+'/'+title+'.'+response.url.split('.')[-1]
        return file_key

    def get_media_requests(self, item, info):
        return scrapy.Request(item['play_path'],meta={'title':item['title']
                                                 ,'name':item['name']})

    def item_completed(self, results, item, info):
        play_path = [x['path'] for ok, x in results if ok]
        if not play_path:
            raise DropItem("Item contains no files")
        item['play_path'] = play_path
        return item

