import tensorflow as tf
import cx_Oracle 
import numpy as np
from google.protobuf.text_format import ParseInteger
from keras.utils import np_utils

class MyRecom:
    def __init__(self):
        self.conn = cx_Oracle.connect("TEAM2_202308F", "java", "112.220.114.130:1521/xe")
        self.curs = self.conn.cursor()
        
    def allMember(self):
        sql =  """
               SELECT *
               FROM EMP_NO, EMP_CMP_ID
        """
        self.curs.execute(sql);
        mylist = self.curs.fetchall()
        self.bookdatalist = mylist
    
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
        
    def __del__(self):
        self.curs.close()
        self.conn.close()
        
if __name__ == '__main__':
        de = MyRecom()
        # emps = de.allMember()
        # emp_no=""
        # emp_cmp_id=""
        #
        # for  e in emps:
        #     emp_no = e['emp_no']
        #     emp_cmp_id = e['cmp_id']
        # ar = AaoRecom(emp_no, emp_cmp_id)
        
        
        # xt,yt = de.getXtYtTrain()
        # print(xt,yt)
        # de.getPred()
        de.getXtYtTest()
