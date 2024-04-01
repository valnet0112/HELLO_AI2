import cx_Oracle as cx
import tensorflow as tf
import numpy as np
from google.protobuf.text_format import ParseInteger
from keras.utils import np_utils

class myRecommend:

    def __init__(self):
        self.conn = cx.connect("TEAM2_202308F/java@112.220.114.130:1521/XE")
        self.curs = self.conn.cursor()
        self.age = [
                        {'label':'0','value':'20'},
                        {'label':'1','value':'30'},
                        {'label':'2','value':'40'},
                        {'label':'3','value':'50'},
                        {'label':'4','value':'60'}
                    ]
        self.ageLength = len(self.age)
        self.deptLength = 0
        self.deptList = []
        self.cerList = []
        self.certificate= []
        
    def select_cer_list(self):
        sql = """
            SELECT *
            FROM CERTIFICATE
        """
        self.curs.execute(sql);
        mylist = self.curs.fetchall()
        self.certificate = mylist
        
        
    def selectEMP_CER_List(self):
        sql = """
            SELECT *
            FROM EMP_CER
        """
        self.curs.execute(sql);
        mylist = self.curs.fetchall()
        self.cerList = mylist
        
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
    
    def getTrains(self):
        self.selectEMP_CER_List()
        self.DeptList()
        cnt = self.ageLength + self.deptLength
        
        sql = f"""
            SELECT 
            TRUNC(MONTHS_BETWEEN(SYSDATE,EMP_BIRTHDAY) /12 ) AS AGE,
            DPT_NAME, A.CER_ID, C.DPT_LABEL
            FROM EMP_CER A JOIN EMPLOYEE B ON (A.EMP_NO = B.EMP_NO AND A.EMP_CMP_ID = B.EMP_CMP_ID)
            JOIN DEPARTMENT C ON (B.EMP_DPT_ID1 = C.DPT_ID)
        """
        
        self.curs.execute(sql);
        
        results = self.curs.fetchall()
        
        x_trains = np.array([],int)
        y_trains = np.array([],int)
        for result in results:
            my = f"{result[0]}"
            myTeam = f"{result[1]}"
            myage = f"{my[:-1]}{0}"
            yLabel = ParseInteger(result[2])
            y_trains = np.append(y_trains,yLabel)
            ageLabel = '' 
            teamLabel = ''
            for i in self.age:
                if i['value']==myage:
                    ageLabel=i['label']
            
            for i in self.deptList:
                if i[0]==myTeam:
                    teamLabel = i[1]
            
            x1 = np_utils.to_categorical(ageLabel,self.ageLength, int)
            x2 = np_utils.to_categorical(teamLabel,self.deptLength, int)
            xt = np.append(x1,x2)
            x_trains = np.append(x_trains,xt)
            
            
        x_trains = np.reshape(x_trains,(-1,cnt))
        return x_trains, y_trains
    
    def makeModel(self):
        x_train, y_train = self.getTrains()
        cnt = self.ageLength + self.deptLength
        self.select_cer_list()

        
        model = tf.keras.Sequential([
                        tf.keras.layers.Flatten(input_shape=(cnt,)),
                        tf.keras.layers.Dense(512, activation = tf.nn.relu),
                        tf.keras.layers.Dense(512, activation = tf.nn.relu),
                        tf.keras.layers.Dense(len(self.certificate), activation=tf.nn.softmax)
                    ])
        model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
        
        model.fit(x_train, y_train, epochs=50)
        model.save('certificate.h5')
        
        
        
        # x_pred = [x_train]
        # pred = model.predict(x_pred)
        # myidx = np.argmax(pred)
        # print(myidx)

        
        pred = model.predict(x_train)
        for p in pred:
            myidx = np.argmax(p)
            print(myidx)
    
    def getRecom(self):
        
        self.selectEMP_CER_List()
        self.DeptList()
        cnt = self.ageLength + self.deptLength
        
        sql = f"""
            SELECT
            DPT_LABEL, DPT_ID
            FROM DEPARTMENT
        """
        # sql = f"""
        #     SELECT 
        #     TRUNC(MONTHS_BETWEEN(SYSDATE,EMP_BIRTHDAY) /12 ) AS AGE, DPT_NAME, DPT_ID
        #     FROM EMPLOYEE JOIN DEPARTMENT ON (EMP_DPT_ID1 = DPT_ID)
        # """
        self.curs.execute(sql);
        results = self.curs.fetchall()
        x_test = np.array([],int)
        
        for result in results:
            teamLabel = result[0]
            print(teamLabel)
            for ages in self.age:
                ageLabel = ages['label']
                x1 = np_utils.to_categorical(ageLabel,self.ageLength, int)
                x2 = np_utils.to_categorical(teamLabel,self.deptLength, int)
                xt = np.append(x1,x2)
                x_test = np.append(x_test,xt)
                
        x_test = np.reshape(x_test,(-1,cnt))
        
        model = tf.keras.models.load_model('certificate.h5')
        pred = model.predict(x_test)
        
        recomArr = []
        ind = 0
        agee = 0
        for idx,p in enumerate(pred):
            if idx % 5 == 0 and idx != 0:
                ind += 1
            
            
            for rank in range(1,4):
                recomTuple = []
            
                recomLabel = np.argmax(p)
                recomTuple.append(results[ind][1])
                recomTuple.append(self.age[agee]['value'])
                recomTuple.append(rank)
                recomTuple.append(recomLabel)
                p[recomLabel] = 0 
                recomArr.append(recomTuple.copy())
                
            agee +=1
            if agee == 5:
                agee = 0
            # print(recomArr)
        return recomArr
    
    
    def reset(self):
        delSql = "DELETE FROM CER_RECOM"
        self.curs.execute(delSql);
        self.conn.commit()
    
    def setRecom(self):
        recomArr = self.getRecom()
        for re in recomArr:
            sql = f"""
                INSERT INTO CER_RECOM
                VALUES('{re[0]}','{re[1]}','{re[2]}','{re[3]}')
            """
            self.curs.execute(sql);
            self.conn.commit()
            
    
    def __del__(self):
        self.curs.close()
        self.conn.close()    
    
    

if __name__ == '__main__':
    de = myRecommend()
    # de.makeModel()
    de.getRecom()
    # de.reset()
    # de.setRecom()
    
    
    
    