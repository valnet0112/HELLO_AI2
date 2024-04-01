import pandas as pd
import numpy as np

# data = pd.read_csv('book.csv')
# print(data.isnull().sum())  #빈칸세줌
# data = data.dropna()             #dropna()는 NaN/빈값있는 행을 제거해줌
data = pd.read_csv('train.csv')
평균 = data['Age'].mean()
print(평균)
최빈값 = data['Embarked'].mode()
print(최빈값)

data['Age'].fillna(value=30, inplace=True)
data['Embarked'].fillna(value='S', inplace=True)
print(data.isnull().sum())
#print(data.isnull().sum())  #빈칸세줌
# data = data.dropna()             #dropna()는 NaN/빈값있는 행을 제거해줌