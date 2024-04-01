import cx_Oracle
import numpy as np
from day01.daomenu import DaoMenu
from google.protobuf.text_format import ParseInteger
from keras.utils import np_utils
import tensorflow as tf


interest = [
    {'label':'0','value':'예술과 문화'},
    {'label':'1','value':'운동과 스포츠'},
    {'label':'2','value':'여행'},
    {'label':'3','value':'과학과 기술'},
    {'label':'4','value':'요리와 음식'},
    {'label':'5','value':'음악'},
    {'label':'6','value':'책과 문학'},
    {'label':'7','value':'사회 문제와 봉사활동'},
    {'label':'8','value':'게임'},
    {'label':'9','value':'자연과 환경'}
]

team = [
    {'label':'0','value':'교육팀'},
    {'label':'1','value':'인사팀'},
    {'label':'2','value':'회계팀'},
    {'label':'3','value':'시설관리팀'},
    {'label':'4','value':'구매팀'},
    {'label':'5','value':'법무팀'},
    {'label':'6','value':'제품기획팀'},
    {'label':'7','value':'제품마케팅팀'},
    {'label':'8','value':'영업1팀'},
    {'label':'9','value':'영업2팀'}
]

class DaoDiet:

    def __init__(self):
        self.conn = cx_Oracle.connect("TEAM2_202308F", "java", "112.220.114.130:1521/xe")
        self.curs = self.conn.cursor()
        self.cnt = len(interest)+len(team)


    def dietList(self):
        sql =   """
                SELECT 
                    EMP_NO, EMP_CMP_ID, EMP_DPT_ID1
                FROM EMPLOYEE
                WHERE EMP_CMP_ID = 'dreaminfosystem'
        """
        self.curs.execute(sql)
        list = self.curs.fetchall()
        myjson =[]
        for e in list:
            myjson.append({'EMP_NO':e[0], 'EMP_CMP_ID':e[1], 'EMP_DPT_ID1':e[2]})
        return myjson  
    
     
    
    def getXtYt(self):
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
            print(result)
            myinterest = f"{result[0]}"
            myteam = f"{result[1]}"
            # yLabel = ParseInteger(result[2])
            yLabel = result[2]
            y_train = np.append(y_train,yLabel)
            interestLength = len(interest)
            interestLabel = ''
            print(interestLength)
            teamLength = len(team)
            teamLabel = ''
            for i in interest:
                if i['value']==myinterest:
                    interestLabel=i['label']
            
            for i in team:
                if i['value']==myteam:
                    teamLabel = i['label']

        
            x1 = np_utils.to_categorical(interestLabel,interestLength, int)
            x2 = np_utils.to_categorical(teamLabel,teamLength, int)
            xt = np.append(x1,x2)
            x_train = np.append(x_train,xt)
        x_train = np.reshape(x_train,(-1,self.cnt))
        return x_train, y_train

        
    def getPred(self):
        x_train, y_train = de.getXtYt()
        

        model = tf.keras.Sequential([
                        tf.keras.layers.Flatten(input_shape=(self.cnt,)),
                        tf.keras.layers.Dense(512, activation = tf.nn.relu),
                        tf.keras.layers.Dense(512, activation = tf.nn.relu),
                        tf.keras.layers.Dense(10, activation=tf.nn.softmax)
                    ])
        model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
        
        model.fit(x_train, y_train, epochs=50)
        model.save('recom1.h5')
        pred = model.predict(x_train)


    
    def __del__(self):
        self.curs.close()
        self.conn.close()

        
if __name__ == '__main__':
    de = DaoDiet()
    dm = DaoMenu()
    xt,yt = de.getXtYt()
    print(xt,yt)
    de.getPred()
