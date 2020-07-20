'''
1. SELECT * FROM data;
print(data)
2. SELECT * FROM data LIMIT 10;
data = data.head(10)
3. SELECT id FROM data;  //id 是 data 表的特定一列
data = data["id"]
4. SELECT COUNT(id) FROM data;
data = data["id"].count()
5. SELECT * FROM data WHERE id<1000 AND age>30;
data = data[(data["id"]>1000) & (data["age"]>31)]
6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
table1.drop_duplicates('order_id',inplace=True)
for group in table1.groupby('id'):
    print(group)
7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
data.merge(table2,how='inner',on='id')
8. SELECT * FROM table1 UNION SELECT * FROM table2;
table1.merge(table2,how='outer')
pandas.concat([table1,table2])
9. DELETE FROM table1 WHERE id=10;
del data[table1['id'] == 10]
10. ALTER TABLE table1 DROP COLUMN column_name;
data.drop(['column_name'],axis=1)
'''


import pandas

data = pandas.read_excel("/Users/lvyz/Downloads/6666.xls")
# data = data[(data["id"]>1000) & (data["age"]>31)]
data = data.drop(['column_name'],axis=1)
print(data)
