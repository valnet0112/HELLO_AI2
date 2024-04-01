import cx_Oracle

class DaoMenu:

    def __init__(self):
        self.conn = cx_Oracle.connect('python/python@localhost:1521/xe')
        self.curs = self.conn.cursor()
        
        
    def getLabels(self):
        sql =   """
            select 
                m_id,
                m_name
            from menu
            order by m_id
        """
        self.curs.execute(sql)
        list = self.curs.fetchall()
        myjson = []
        for e in list:
            myjson.append({'m_id':e[0],'m_name':e[1]})
        return myjson

    def menuList(self):
        sql =   """
            select 
                m_id,
                m_name,
                DECODE(use_yn, 'y', 'O', 'n', 'X', '-') use_yn
            from menu
        """
        self.curs.execute(sql)
        list = self.curs.fetchall()
        myjson = []
        for e in list:
            myjson.append({'m_id':e[0],'m_name':e[1],'use_yn':e[2]})
        return myjson
    
    def getCnt(self):
        sql =   """
            select
                count(*) as cnt
            from menu
                
        """
        self.curs.execute(sql)
        list = self.curs.fetchall()
        return list[0][0]
    
    
    def __del__(self):
        self.curs.close()
        self.conn.close()

        
if __name__ == '__main__':
    dm = DaoMenu()
    cnt = dm.getLabels()
    print(cnt)
