import cx_Oracle

class DaoRecom:
    def __init__(self):
        self.conn = cx_Oracle.connect('python/python@localhost:1521/xe')
        self.curs = self.conn.cursor()
        
    def insertRecom(self,e_id,m_id):
        sql =f"""
            INSERT INTO 
                RECOM(E_ID,M_ID,YMD) 
            VALUES('{e_id}','{m_id}',TO_CHAR(SYSDATE, 'YYYYMMDD'))
        """
            
        self.curs.execute(sql)
        self.conn.commit() 
        return self.curs.rowcount
    
    def __del__(self):
        self.curs.close()
        self.conn.close()
        
if __name__ == '__main__':
    dr = DaoRecom()
    cnt= dr.insertRecom('S001','2')
    print(cnt)
