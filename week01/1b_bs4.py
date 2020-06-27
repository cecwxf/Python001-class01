# 使用BeautifulSoup解析网页

import requests
from bs4 import BeautifulSoup as bs
# bs4是第三方库需要使用pip命令安装


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.3904.108 Safari/537.36'

header = {'user-agent':user_agent}

myurl = 'https://maoyan.com/board/4'

response = requests.get(myurl,headers=header)
print("实际链接: " + response.url)
response.close()
bs_info = bs(response.text, 'html.parser')

filmname = []
releasetime = []
# Python 中使用 for in 形式的循环,Python使用缩进来做语句块分隔
for tags in bs_info.find_all('p', attrs={'class': 'name'}):
    for atag in tags.find_all('a',):
        filmname.append(atag.get('title'))
        # print(atag.get('title'))

for tags in bs_info.find_all('p', attrs={'class': 'releasetime'}):
        # releasetime.append(tags.text)
        releasetime.append(tags.text)
        # print(tags.text)

# myList = [filmname, releasetime]

title_list = bs_info.find_all('div', attrs={'class': 'movie-item-info'})

myList = {}
for i in title_list:
        title = i.find('a').get('title')
        link = i.find('a').get('href')
        releasetime = i.find('p',attrs={'class' : 'releasetime'}).text
        myList['title'] = title
        myList['link'] = link
        myList['releasetime'] = releasetime
        print(myList['title'] + myList['link'] + myList['releasetime'])


import pandas as pd

movie1 = pd.DataFrame(data = [myList])

movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=False)
