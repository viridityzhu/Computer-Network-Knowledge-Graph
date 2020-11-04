import scrapy
from MyCrawler.items import HudongItem
import urllib
import re

split_sign = '##'  # 定义分隔符


class HudongSpider(scrapy.Spider):
    name = "hudong"  # 爬虫启动命令：scrapy crawl hudong
    allowed_domains = ["www.baike.com"]  # 声明地址域

#	file_object = open('merge_table3.txt','r').read()
    file_object = open('leaf_from_baidu.csv', 'r').read()
    wordList = file_object.split()  # 获取词表

    start_urls = []
    count = 0

#	start_urls.append('http://www.baike.com/wiki/小米%5B农作物%5D')
#	start_urls.append('http://www.baike.com/wiki/苹果%5B果实%5D')
#	start_urls.append('http://www.baike.com/wiki/李%5B蔷薇科李属植物%5D')

  # 本处是用于构造原始json
    for i in wordList:  # 生成url列表
        cur = "http://www.baike.com/wiki/"
        cur = cur + str(i)
        start_urls.append(cur)
#		count += 1
#		#print(cur)
#		if count > 1000:
#			break

    def parse(self, response):
        # div限定范围

        main_info = response.css('body script::text').extract()[0]

        title = response.url.split('/')[-1]  # 通过截取url获取title
        title = urllib.parse.unquote(title)

        url = response.url   # url直接得到
        url = urllib.parse.unquote(url)
        try:
            im = re.findall(
                r'"summary_image\\.*?"url.*?".*?".*?"', main_info)[0]
            img = re.findall(r'//.*image', im)[0]
        except:
            img = ''
        # openTypeList = ""  # 爬取开放域标签
        # flag = 0  # flag用于分隔符处理（第一个词前面不插入分隔符）
        # for p in main_div.xpath('.//div[@class="l w-640"]/div[@class="place"]/p[@id="openCatp"]/a/@title'):
        #     if flag == 1:
        #         openTypeList += split_sign
        #     openTypeList += p.extract().strip()
        #     flag = 1

        detail = re.findall(
            r'<meta content=".*?" name="description">', response.text)[0][15:-21]
        # flag = 0
        # baseInfoKeyList = ""  # 基本信息的key值
        # for p in main_div.xpath('.//div[@class="l w-640"]/div[@name="datamodule"]/div[@class="module zoom"]/table//strong/text()'):
        #     if flag == 1:
        #         baseInfoKeyList += split_sign
        #     baseInfoKeyList += p.extract().strip()
        #     flag = 1

        # 继续调xpath！！！！！！！！！！！！！
        # flag = 0
        # baseInfoValueList = ""  # 基本信息的value值
        # base_xpath = main_div.xpath(
        #     './/div[@class="l w-640"]/div[@name="datamodule"]/div[@class="module zoom"]/table')
        # for p in base_xpath.xpath('.//span'):
        #     if flag == 1:
        #         baseInfoValueList += split_sign
        #     all_text = p.xpath('string(.)').extract()[0].strip()
        #     baseInfoValueList += all_text
        #     flag = 1

        item = HudongItem()
        item['title'] = title
        item['url'] = url
        item['image'] = img
        # item['openTypeList'] = openTypeList
        item['detail'] = detail
        # item['baseInfoKeyList'] = baseInfoKeyList
        # item['baseInfoValueList'] = baseInfoValueList

        yield item
