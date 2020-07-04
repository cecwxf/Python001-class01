# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import Demo3Item
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    # start_urls = ['https://maoyan.com/films?showType=3']

    # def parse(self, response):
    #     pass
     # 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象（Request）。
    # start_requests()方法读取start_urls列表中的URL并生成Request对象，发送给引擎。
    # 引擎再指挥其他组件向网站服务器发送请求，下载网页
    def start_requests(self):
        # for i in range(0, 2):
            url = 'https://maoyan.com/films?showType=3'
            yield scrapy.Request(url=url, callback=self.parse)
            # url 请求访问的网址
            # callback 回调函数，引擎回将下载好的页面(Response对象)发给该方法，执行数据解析
            # 这里可以使用callback指定新的函数，不是用parse作为默认的回调参数

    # 解析函数
    def parse(self, response):
        print("实际链接:" + response.url)
        # print(response.content)
        # soup = BeautifulSoup(response.text, 'html.parser')
        # title_list = soup.find_all('div', attrs={'class': 'movie-item-info'})
        # #for i in range(len(title_list)):
        # 在Python中应该这样写
        # select each movie
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]')
        for movie in movies[:10]:
            try:
                movie_infos = movie.xpath('.//div[contains(@class,"movie-hover-title")]')

                movie_title_selector = movie_infos[0].xpath('./@title')
                movie_title = movie_title_selector.extract_first()
                movie_type_selector = movie_infos[1].xpath('./text()')
                movie_type = movie_type_selector.extract()[1].strip()
                release_date_selector = movie_infos[3].xpath('./text()')
                release_date = release_date_selector.extract()[1].strip()

                # init new item for each movie
                item = Demo3Item()
                item['movie_title'] = movie_title
                item['movie_type'] = movie_type
                item['release_date'] = release_date
            except Exception as e:
                print(e)
            finally:
                yield item

    # # 解析具体页面
    # def parse2(self, response):
    #     item = response.meta['item']
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     content = soup.find('div', attrs={'class': 'board-item-main'}).get_text().strip()
    #     item['content'] = content
    #     yield item