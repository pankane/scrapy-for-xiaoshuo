# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import json

curTime = time.strftime("%Y-%m-%d", time.localtime())


class XiaoshuoPipeline(object):

    def process_item(self, item, spider):
        pageStart = item['page']
        self.file = open('pageNumber.jl', 'wb')
        line = json.dumps(item['page']) + '\n'
        self.file.write(line)
        with open('novelName.jl', 'r') as name:
            novelName = name.readline()
            novelName = novelName.rstrip()
            
        with open(novelName + str(curTime) + '.txt', 'a+') as file:
            title = item['title'][0].encode('utf-8')
            content = item['content']
            file.write(title + '\n\n')
            for i in range(len(content)):
                article = content[i].encode('utf-8')
                file.write(article)
                file.write('\n\n\n')
        return item
