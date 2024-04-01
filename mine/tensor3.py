import tensorflow as tf


train_x=[1,2,3,4,5,6,7]
train_y=[3,5,7,9,11,13,15]

a=tf.Variable(0.1)
b=tf.Variable(0.1)


def 손실함수(a, b):
    예측_y = train_x * a + b             # 1.모델만들기
    return tf.keras.losses.mse(train_y, 예측_y)
opt = tf.keras.optimizers.Adam(learning_rate=0.001)   #2. optimizer 손실함수 정하기

for i in range(9000):                              #3. 학습하기(경사하강으로 변수값 업데이트하기)
    opt.minimize(lambda:손실함수(a,b), var_list=[a,b])
    print(a.numpy(),b.numpy())


