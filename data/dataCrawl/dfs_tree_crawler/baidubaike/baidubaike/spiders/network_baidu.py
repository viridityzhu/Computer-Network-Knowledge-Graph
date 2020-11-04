# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from baidubaike.items import BaidubaikeItem
from bs4 import BeautifulSoup
import re
from urllib import parse


class NetworkBaiduSpider(scrapy.Spider):
    name = 'network_baidu'
    allowed_domains = ['baike.baidu.com']
    start_urls = [
        'https://baike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E6%8A%80%E6%9C%AF/1194', 'https://baike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/18763']

    def parse(self, response):
        res_data = BaidubaikeItem()

        # res_data['url'] = response.url
        soup = BeautifulSoup(response.body, 'html.parser',
                             from_encoding="utf-8")
        try:
            title_node = soup.find(
                'span', class_="lemma-title")
            res_data['title'] = title_node.get_text()
        except:
            title_node = soup.find(
                'dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
            res_data['title'] = title_node.get_text()

        yield res_data
        links = soup.find_all('a', href=re.compile(r"/item/.+"))
        for link in links:
            new_url = link['href']
            new_full_url = parse.urljoin(response.url, new_url)

            yield Request(new_full_url)
