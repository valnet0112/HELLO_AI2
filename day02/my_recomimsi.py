import tensorflow as tf
import cx_Oracle 
import numpy as np
from google.protobuf.text_format import ParseInteger
from keras.utils import np_utils

class MyRecom:
    def __init__(self):
        self.conn = cx_Oracle.connect("TEAM2_202308F", "java", "112.220.114.130:1521/xe")
        self.curs = self.conn.cursor()
        self.deptLength = 0
        self.bookdatalist = []
        self.selectreadinghistory= []
        self.interestList = []
        self.interestLength = 0
        self.deptList = []
    
    def selectbookdatalist(self):
        sql =  """
               SELECT *
               FROM BOOKDATA
        """
        self.curs.execute(sql);
        mylist = self.curs.fetchall()
        self.bookdatalist = mylist
        
    def selectreadinghistorya(self):
        sql =  """
               SELECT *
               FROM READINGHISTORY
        """
        self.curs.execute(sql);
        mylist = self.curs.fetchall()
        self.readinghistory = mylist
        
    def selectInterestList(self):
        sql = f"""
            SELECT 
            IN_NAME, IN_LABEL
            from INTEREST
        """
        self.curs.execute(sql)
        mylist = self.curs.fetchall()
        self.interestLength = len(mylist)
        self.interestList = mylist
    def DeptList(self):
        sql = f"""
            SELECT 
            DPT_NAME, DPT_LABEL
            from 
            DEPARTMENT
        """
        self.curs.execute(sql)
        mylist = self.curs.fetchall()
        self.deptLength = len(mylist)
        self.deptList = mylist
        
    def getXtYtTrain(self):
        self.selectbookdatalist()
        self.selectInterestList()
        self.selectreadinghistorya()
        self.DeptList()
        cnt = self.interestLength + self.deptLength
        sql =   f"""
                SELECT 
                    EMP_INTERESTS, DPT_NAME, RH_BD_ID
                FROM 
                    READINGHISTORY JOIN EMPLOYEE ON (RH_EMP_NO = EMP_NO AND RH_CMP_ID = EMP_CMP_ID)
                    JOIN DEPARTMENT  ON (EMP_DPT_ID1 = DPT_ID)

        """
        self.curs.execute(sql)
        results = self.curs.fetchall()
        
        
        x_train = np.array([],int)
        y_train = np.array([],int)
        for result in results:
            myinterest = f"{result[0]}"
            myteam = f"{result[1]}"
            yLabel = result[2]
            y_train = np.append(y_train,yLabel)
            interestLabel = ''
            teamLabel = ''
            for i in self.interestList:
                if i[0]==myinterest:
                    interestLabel=i[1]
                    print("asdasdsadasdasdasdad",interestLabel)
            for i in self.deptList:
                if i[0]==myteam:
                    teamLabel = i[1]
                    print("team_label",teamLabel)
        
            x1 = np_utils.to_categorical(interestLabel,self.interestLength, int)
            x2 = np_utils.to_categorical(teamLabel,self.deptLength, int)
            xt = np.append(x1,x2)
            x_train = np.append(x_train,xt)
        x_train = np.reshape(x_train,(-1,cnt))
        return x_train, y_train
    
    # def getPred(self):
    #     x_train, y_train = self.getXtYtTrain()
    #     cnt = self.interestLength + self.deptLength
    #
    #
    #     model = tf.keras.Sequential([
    #                     tf.keras.layers.Flatten(input_shape=(cnt,)),
    #                     tf.keras.layers.Dense(512, activation = tf.nn.relu),
    #                     tf.keras.layers.Dense(512, activation = tf.nn.relu),
    #                     tf.keras.layers.Dense(len(self.readinghistory), activation=tf.nn.softmax)
    #                 ])
    #     model.compile(optimizer='adam',
    #           loss='sparse_categorical_crossentropy',
    #           metrics=['accuracy'])
    #
    #     model.fit(x_train, y_train, epochs=50)
    #     model.save('recom.h5')
    #     pred = model.predict(x_train) 
    #     for p in pred:
    #         myidx = np.argmax(p)
    #         print(myidx)   
    #
    #     x_rf = self.dd.getPred(self.e_id, self.cnt)
    #     pred_rf = model.predict(x_rf)
    #     myidx = np.argmax(pred_rf)
    #     recom_menu = self.labels[myidx]['m_name']
    #     recom_m_id = self.labels[myidx]['m_id']
    #
    #
    #     self.dr.insertRecom(self.e_id, recom_m_id)
    #

        
    def __del__(self):
        self.curs.close()
        self.conn.close()
        
if __name__ == '__main__':
        de = MyRecom()
        xt,yt = de.getXtYtTrain()
        print(xt,yt)
        # de.getPred()
