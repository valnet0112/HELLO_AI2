import tensorflow as tf
import numpy as np
from day01.daodiet import DaoDiet
from day01.daomenu import DaoMenu
from day01.daorecom import DaoRecom
import datetime
from day01.daoemp import DaoEmp

class AaoRecom:
    def __init__(self,e_id):
        self.dm = DaoMenu()
        self.dd = DaoDiet()
        self.dr = DaoRecom()
        
        self.e_id=e_id
        self.labels = self.dm.getLabels()
        self.x_train = None
        self.y_train = None
        self.cnt = self.dm.getCnt()
        self.setXYTrain(self.e_id,self.cnt)
        
    def setXYTrain(self, e_id , cnt):
        self.x_train, self.y_train = self.dd.getXtYt(e_id, cnt)
        

    def pred(self):
        
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(self.cnt*2,)),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dense(self.cnt, activation=tf.nn.softmax)
        ])
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        
        model.fit(self.x_train, self.y_train, epochs=20)
        model.save('recom.h5')
        
        pred = model.predict(self.x_train)
        
        for p in pred:
            myidx = np.argmax(p)
            print("myidx",myidx)
        
        x_rf = self.dd.getPred(self.e_id, self.cnt)
        pred_rf = model.predict(x_rf)
        myidx = np.argmax(pred_rf)
        print(myidx)
        recom_menu = self.labels[myidx]['m_name']
        recom_m_id = self.labels[myidx]['m_id']
        
        now = datetime.datetime.now()
        ymd = now.strftime("%Y%m%d_%H%M")
        
        self.dr.insertRecom(self.e_id, recom_m_id)
        
        
    def __del__(self):
        print("소멸자")
        
if __name__ == '__main__':
    de = DaoEmp()
    list = de.selectList()
    
    for e in list:
        e_id = e['e_id']
        print(e_id)
        ar = AaoRecom(e_id)
        ar.pred()