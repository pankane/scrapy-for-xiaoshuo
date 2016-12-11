#!/usr/bin/env python
# coding=utf-8
#!/usr/bin/env python
# coding=utf-8
from scrapy.spider import Spider
from scrapy.selector import Selector
from xiaoshuo.items import XiaoshuoItem
from scrapy.http import Request
import json
import glob
import os

from scrapy import signals
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class xiaoshuo(Spider):
    name = "xiaoshuo"
    with open("pageNumber.jl") as jsonfile:
        page = json.load(jsonfile)
   # page = input('Please input page number:')
    startUrl = "http://www.uukanshu.com" + \
        str(page)

    allowed_domains = ["www.uukanshu.com"]
    start_urls = [startUrl]

    def parse(self, response):
        item = XiaoshuoItem()
        sel = Selector(response)

        oldUrl = sel.xpath('//div[@class = "fanye_cen"]/a/@href').extract()

        newUrl = "http://www.uukanshu.com" + oldUrl[0]

        if newUrl[-1] != "/":
            item['page'] = oldUrl[0]
            yield Request(newUrl, callback=self.parse)

        else:
            item['page'] = response.url[23:]
            print('下载完成')

        item['content'] = sel.xpath(
            '//div[@id="contentbox"]/text()|//div[@id="contentbox"]/p/text()').extract()
        item['title'] = sel.xpath(
            '//div[@class = "h1title"]/h1/text()').extract()

        yield item

    @classmethod
    def from_crawler(cls, crawler):
        spider = cls()
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        from_addr = ('email@email.com')
        password = ('password')
        smtp_server = ('smtp-mail.outlook.com')
        to_addr = ('xxxxxx@kindle.com')
        msg = MIMEMultipart()
        msg.attach(MIMEText('xiaoshuo', 'plain', 'utf-8'))

        fileName = glob.glob('*.txt')[0]
        with open(fileName, 'rb') as f:
            mime = MIMEBase('text', 'plain', filename=fileName)
            mime.add_header(
                'Content-Disposition',
                'attachment',
                filename=fileName)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-ID', '0')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)

        server = smtplib.SMTP(smtp_server, 587)
       # server.set_debuglevel(1)
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        os.remove(fileName)
