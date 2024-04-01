import pandas as pd
import numpy as np

data = pd.read_csv('gpascore.csv')
#print(data.isnull().sum())  #빈칸세줌
data = data.dropna()             #dropna()는 NaN/빈값있는 행을 제거해줌
exit(data)

y데이터 = data['admit'].values
print(y데이터)
x데이터 = []

for i, rows in data.iterrows():
   x데이터.append([rows['gre'], rows['gpa'], rows['rank']]) 
print(x데이터)
   
   
import tensorflow as tf

model = tf.keras.models.Sequential([         
    tf.keras.layers.Dense(64, activation='tanh'),
    tf.keras.layers.Dense(128, activation='tanh'),
    tf.keras.layers.Dense(1, activation='sigmoid') #마지막 레이어는 0~1사이의 확률을 뱉고 싶으면 sigmoid 사용
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(np.array(x데이터), np.array(y데이터), epochs=1000)  #모델학습시키기 x는 학습데이터 y는 실제 정답


#예측
예측값 = model.predict([[750,3.70,3],[400,2.2,1]])
print(예측값)

