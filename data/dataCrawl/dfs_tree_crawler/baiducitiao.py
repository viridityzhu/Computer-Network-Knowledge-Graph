# -*- coding: utf-8 -*-
"""
从百度百科python词条开始，爬取1000个词条页面，得到词条URL、词条名和词条简介，输出并保存为HTML文档
程序入口、爬虫调度器，
"""
import csv


class SpiderMain(object):

    def __init__(self):
        self.urls = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.outputer = HtmlOutputer()

    def craw(self, root_url):
        """调用url管理、网页下载、网页解析和结果输出"""
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("craw %d : %s" % (count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                print(self.urls.new_urls)
                self.outputer.collect_data(new_data)
                if count == 1000:
                    break
                count += 1
                self.outputer.output_html()
            except Exception as e:
                print("craw failed", new_url, e)


"""
URL管理
"""


class UrlManager(object):

    def __init__(self):
        """初始化已爬取URL集合、未爬取URL集合"""
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url):
        """添加未爬取URL"""
        if url is None:
            return
        if (url not in self.new_urls) and (url not in self.old_urls):
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        """批量添加未爬取URL"""
        if (urls is None) or (len(urls) == 0):
            return
        for url in urls:
            self.add_new_url(url)

    def get_new_url(self):
        """取出未爬取URL并添加至已爬取URL集合"""
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def has_new_url(self):
        """确认是否还有未爬取URL"""
        return len(self.new_urls) != 0
"""
网页下载
"""

from urllib import request


class HtmlDownloader(object):

    def download(self, url):
        """使用urllib.request.urlopen()下载网页内容"""
        if url is None:
            return None
        response = request.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read().decode("utf-8")

"""
网页解析
"""

from bs4 import BeautifulSoup
import re
from urllib import parse


class HtmlParser(object):
    new_urls = set()  # 解析出的URL集合

    def __get_new_urls(self, page_url, soup):
        """根据网页内容，解析出网页中词条URL"""
        links = soup.find_all('a', href=re.compile(r"/item/.+"))
        for link in links:
            new_url = link['href']
            new_full_url = parse.urljoin(page_url, new_url)
            HtmlParser.new_urls.add(new_full_url)
        return HtmlParser.new_urls

    def __get_new_data(self, page_url, soup):
        """根据网页内容，解析出词条名和词条简介"""
        res_data = dict()

        res_data['url'] = page_url
        try:
            title_node = soup.find(
                'span', class_="lemma-title")
            res_data['title'] = title_node.get_text()
        except:
            title_node = soup.find(
                'dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
            res_data['title'] = title_node.get_text()

        summary_node = soup.find('div', class_="summary-content")
        # res_data['summary'] = summary_node.get_text()

        return res_data

    def parse(self, page_url, html_cont):
        """返回解析出的新URL集合和词条名、词条简介"""
        if (page_url is None) or (html_cont is None):
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding="utf-8")
        # print(html_cont)
        new_urls = self.__get_new_urls(page_url, soup)
        new_data = self.__get_new_data(page_url, soup)
        return new_urls, new_data
"""
结果保存
"""


class HtmlOutputer(object):

    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        """将不同词条页URL、词条名和词条简介添加至一个列表"""
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        """将结果输出为csv文件"""
        with open("leaf_from_baidu.csv", 'w') as f:
            w = csv.writer(f)
            for data in self.datas:
                w.writerow([data[key] for key in data.keys()])


if __name__ == "__main__":
    root_url = "https://wapbaike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/18763"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
