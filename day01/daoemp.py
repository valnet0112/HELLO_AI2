import cx_Oracle

class DaoEmp:

    def __init__(self):
        self.conn = cx_Oracle.connect('python/python@localhost:1521/xe')
        self.curs = self.conn.cursor()

    def selectList(self):
        sql =   """
                select 
                    e_id, 
                    e_name, 
                    DECODE(gen, 'm', '남자', 'f', '여자', '기타')gen, 
                    addr    
                from emp
        """
        self.curs.execute(sql)
        list = self.curs.fetchall()
        myjson =[]
        for e in list:
            myjson.append({'e_id':e[0], 'e_name':e[1], 'gen':e[2], 'addr':e[3]})
        return myjson
    
         
   
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
    
    
    def __del__(self):
        self.curs.close()
        self.conn.close()

        
if __name__ == '__main__':
    de = DaoEmp()
    list = de.dietList()
    print(list)
