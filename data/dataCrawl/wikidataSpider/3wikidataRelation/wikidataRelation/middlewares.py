# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class ProxyMiddleware(object):

    def process_request(self, request, spider):

        request.meta['proxy'] = 'http://127.0.0.1:1084'
        spider.logger.info('request.meta {}'.format(request.meta))
