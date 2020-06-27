# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd

class Demo3Pipeline:
    def process_item(self, item, spider):
        title = item['title']
        link = item['link']
        releasetime = item['releasetime']
        print("hello wxf!!!!!!!!!!!!!!!!!!!!!!!!!")
        output = f'|{title}|\t|{link}|\t|{releasetime}|\n\n'
        movie1 = pd.DataFrame(data = output)
        movie1.to_csv('./movie_maoyan.csv', mode='a', encoding='utf8', index=False, header=False)
        return item
