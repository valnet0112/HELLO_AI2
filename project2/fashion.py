import tensorflow as tf
import matplotlib.pyplot as plt

(trainX, trainY), (testX, testY) = tf.keras.datasets.fashion_mnist.load_data()

# print(trainX[0])
# print(trainX.shape)
#
# print(trainY)

# plt.imshow(trainX[1])
# plt.gray()
# plt.colorbar()
# plt.show()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, input_shape=(28,28), activation="relu"), #relu:음수를 다 0으로 만들어주셈
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Flatten(),                    #행렬을 1차원으로 압축해줌
    tf.keras.layers.Dense(10, activation="softmax"), #0~1까지 확률을 압축시킬떄 sigmoid는 binary예측문제에 사용 0인지 1인지 붙는다 안붙는다 예측할때 마지막 노드갯수는 1개 ,,,,여러가지 카테고리예측문제softmax: 10개의카테고리
])
model.summary()


model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
model.fit(trainX, trainY, epochs=5)
