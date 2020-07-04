# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import pymysql

dbInfo = {
    'host' : 'localhost',
    'port' :  3306,
    'user' : 'root',
    'password' : 'rootroot',
    'db' : 'geektime_python_train'
}

# sqls = ['select 1', 'select VERSION()']

result = []

sql1 = """CREATE TABLE IF NOT EXISTS movies(
      id int NOT NULL AUTO_INCREMENT,
      movie_title val(200) NOT NULL,
      movie_type val(50) NOT NULL,
      release_date val(100) NOT NULL,
      PRIMARY KET (id))
      ENGINE = MyIASM AUTO_INCREMENT = 1 DEFAULT  CHARSET = utf8mb4"""

class ConnDB(object):
    def __init__(self, dbInfo, sqls,data):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        self.sqls = sqls
        self.data = data

    def run(self):
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db
        )

        cur = conn.cursor()
        # cur.execute(sql1)
        try:
            # for command in self.sqls:
            cur.executemany(self.sqls,self.data)
            result.append(cur.fetchone())
            
            cur.close() 
            conn.commit()
        except:
            conn.rollback()

        conn.close()

class Demo3Pipeline:
    def process_item(self, item, spider):
        movie_title = item['movie_title']
        movie_type = item['movie_type']    
        release_date = item['release_date']
        # output = str(movie_title) + ',' + str(movie_type) + ',' + str(release_date) + '\n'
        # with open('./movie.csv','a+', encoding='UTF-8') as file:
        #     file.write(output)
        # movie = pd.DataFrame([item])
        # movie.to_csv('movie.csv', mode = 'a', encoding="utf8")
        # for id in (1,10):
            # id_item = str(id)
        # sqls = ['INSERT INTO ' + 'week02_maoyan_movie ' +' values(1,f'({movie_title},{movie_type},{release_date})+";"]
        id = 0
        data = [(str(id),movie_title,movie_type,release_date)]
        id = id + 1
        sql2 = """
        INSERT INTO week02_maoyan_movie VALUES(%s,%s,%s,%s)"""
        db = ConnDB(dbInfo,sql2,data)
        db.run()
        db = ConnDB(dbInfo,sql1,data)
        db.run()
        # print(result)

        return item
