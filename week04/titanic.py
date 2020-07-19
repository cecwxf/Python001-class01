import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn import tree
df=pd.read_csv('train.csv')
print(df.head())
print(df.info())