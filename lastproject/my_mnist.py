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
                    EMP_INTERESTS, DPT_LABEL, RH_BD_ID
                FROM 
                    READINGHISTORY JOIN EMPLOYEE ON (RH_EMP_NO = EMP_NO AND RH_CMP_ID = EMP_CMP_ID)
                    JOIN DEPARTMENT  ON (EMP_DPT_ID1 = DPT_ID)

        """
        self.curs.execute(sql)
        results = self.curs.fetchall()
        
        
        x_train = np.array([],int)
        y_train = np.array([],int)
        for result in results: 
            xt = np.array([])
            x1 = np_utils.to_categorical(result[0],self.interestLength, int)
            x2 = np_utils.to_categorical(result[1],self.deptLength, int)
            xt = np.append(x1,x2)
            x_train = np.append(x_train,xt)
            y_train = np.append(y_train,result[2])
            
        x_train = np.reshape(x_train,(-1,cnt))
        
        return x_train, y_train
    
    def getPred(self):
        x_train, y_train = self.getXtYtTrain()
        cnt = self.interestLength + self.deptLength
    
    
        model = tf.keras.Sequential([
                        tf.keras.layers.Flatten(input_shape=(cnt,)),
                        tf.keras.layers.Dense(1024, activation = tf.nn.relu),
                        tf.keras.layers.Dense(2048, activation = tf.nn.relu),
                        tf.keras.layers.Dense(len(self.bookdatalist), activation=tf.nn.softmax)
                    ])
        model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
    
        model.summary()
        model.fit(x_train, y_train, epochs=1000)
        model.save('recom.h5')
        pred = model.predict(x_train) 
        # for p in pred:
        #     myidx = np.argmax(p)
        #     print(myidx)   
        #     p[myidx] = 0
        #     myidx = np.argmax(p)
        #     print(myidx)   
        #     p[myidx] = 0
        #     myidx = np.argmax(p)
        #     print(myidx)   
        #     print('=====================')
            
    def getXtYtTest(self):
        self.selectbookdatalist()
        self.DeptList()
        self.selectInterestList()
        cnt = self.interestLength + self.deptLength
        
        # sql = f"""
        #     SELECT 
        #         EMP_INTERESTS, DPT_LABEL, DPT_NAME
        #     FROM 
        #         EMPLOYEE JOIN DEPARTMENT ON (EMP_DPT_ID1 = DPT_ID)
        # """
        # self.curs.execute(sql);
        # results = self.curs.fetchall()
        
        
        x_test = np.array([],int)
        recomResult = []
        for inter in self.interestList:
            for dep in self.deptList:
                re = []
                re.append(inter[1])
                re.append(dep[1])
                recomResult.append(re.copy())
                xt = np.array([])
                x1 = np_utils.to_categorical(inter[1],self.interestLength, int)
                x2 = np_utils.to_categorical(dep[1],self.deptLength, int)
                xt = np.append(x1,x2)
                x_test = np.append(x_test,xt)
      
        x_test = np.reshape(x_test,(-1,cnt))
            
        model = tf.keras.models.load_model('recom.h5')
        
        pred = model.predict(x_test)
        recomArr = []
        ranks = range(1, 4) 
        for idx, p in enumerate(pred):
            for rank in ranks:
                copys = []
                recomLabel = np.argmax(p)
                copys.append(recomResult[idx][0])
                copys.append(recomResult[idx][1])
                copys.append(rank)
                copys.append(recomLabel)
                recomArr.append(copys.copy())
                p[recomLabel] = 0
                
        for k in recomArr:
            print(k)
        return recomArr
    
    def reset(self):
        delSql = "DELETE FROM BOOKRECOM"
        self.curs.execute(delSql)
        self.conn.commit()
        
        
        # for p in pred:
        #     bookLabel1 = np.argmax(p)
        #     p[bookLabel1] = 0 
        #     bookLabel2 = np.argmax(p)
        #     p[bookLabel2] = 0 
        #     bookLabel3 = np.argmax(p)
    
    def insertRecom(self):  
        recomArr = self.getXtYtTest()
        for re in recomArr:
            sql = f"""
                INSERT INTO BOOKRECOM (br_dpt_id, br_emp_interest, br_rank, br_bd_id)
                VALUES ('{re[0]}', '{re[1]}', {re[2]}, {re[3]})
            """
            self.curs.execute(sql);
            self.conn.commit()
       

        
    def __del__(self):
        self.curs.close()
        self.conn.close()
        
if __name__ == '__main__':
        de = MyRecom()
        xt,yt = de.getXtYtTrain()
        de.getPred()
        # de.getXtYtTest()
        # de.reset()
        # de.insertRecom()
        
