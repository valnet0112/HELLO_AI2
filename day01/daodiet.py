import cx_Oracle
import numpy as np
from day01.daomenu import DaoMenu

class DaoDiet:

    def __init__(self):
        self.conn = cx_Oracle.connect('python/python@localhost:1521/xe')
        self.curs = self.conn.cursor()

    def dietList(self):
        sql =   """
                SELECT EMP.E_NAME, MENU.M_NAME, YMD
                FROM DIET JOIN EMP ON (DIET.E_ID = EMP.E_ID)
                        JOIN MENU ON (DIET.M_ID=MENU.M_ID)
                ORDER BY YMD DESC
        """
        self.curs.execute(sql)
        list = self.curs.fetchall()
        myjson =[]
        for e in list:
            myjson.append({'e_id':e[0], 'm_id':e[1], 'ymd':e[2]})
        return myjson  
    def menuList(self):
        sql =   """
                SELECT 
                    M_ID, M_NAME, DECODE(USE_YN, 'y', 'O', 'n', 'X', '기타')USE_YN
                FROM MENU

        """
        self.curs.execute(sql)
        list = self.curs.fetchall()
        myjson =[]
        for e in list:
            myjson.append({'m_id':e[0], 'm_name':e[1], 'use_yn':e[2]})
        return myjson  
    
    def getXtYt(self, e_id,cnt):
        sql =   f"""
                select m_id
                from diet
                where E_ID = '{e_id}'
                order by YMD desc

        """
        self.curs.execute(sql)
        list = self.curs.fetchall()
        arr = []
        for i in list:
            arr.append(i[0])
        
        xtr=[]
        xt=[]
        yt=[]
        for i in range(len(arr)-2):
            yt.append(arr[i])
            xt.append(arr[i+2])
            xt.append(arr[i+1])
            
        for i in range(len(xt)):    
            line_n = np.zeros(cnt).astype(int)
            line_n[xt[i]] = 1
            for l in line_n:
                xtr.append(l)
            
        x_train = np.array(xtr)
        y_train = np.array(yt)
        
        x_train = np.reshape(x_train,(-1,2*cnt))
        
        return x_train,y_train
    def getPred(self,e_id,cnt):
        sql =   """
                select m_id
                from diet
                where E_ID = 'S001'
                order by YMD desc

        """
        self.curs.execute(sql)
        list = self.curs.fetchall()
        arr = []
        for i in list:
            arr.append(i[0])
        
        line_n1 = np.zeros(cnt).astype(int)
        line_n1[arr[1]]=1
        
        line_n2 = np.zeros(cnt).astype(int)
        line_n2[arr[0]]=1
        ret = np.concatenate((line_n1,line_n2))
        return ret
    
    def __del__(self):
        self.curs.close()
        self.conn.close()

        
if __name__ == '__main__':
    de = DaoDiet()
    dm = DaoMenu()
    ret = de.getXtYt('S001', 5)
    
    print(ret)
