import email
from email.utils import parseaddr
from email.header import decode_header, make_header
import imaplib
import smtplib
import numpy as np
import cx_Oracle
from nltk.stem import PorterStemmer, porter

class Mygetgmail:
    def __init__(self):
        self.conn = cx_Oracle.connect("TEAM2_202308F", "java", "112.220.114.130:1521/xe")
        self.curs = self.conn.cursor()
        self.word_map = []

    spam_keywords = ''
    def check_spam(self, body):
        # 스팸으로 분류할 키워드와 그에 대응하는 카테고리를 정의
        spam_keywords = ['광고', '사다리', '마케팅', '이벤트', '판매안내', '할인정보', '특가상품', '홍보', '공지사항', '상품홍보']

        for keyword in spam_keywords:
            if keyword in body:
                return 0  # 키워드가 하나라도 들어가면 스팸으로 판별

        return 1  # 키워드가 하나도 들어가지 않으면 스팸이 아닌 것으로 판별
    def fetch_recent_email(self):
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        imap.login('valnet0112@gmail.com', 'dofz whgf vrdu hmsj')
        imap.select("INBOX")
        
        # 사서함의 모든 메일의 uid 정보 가져오기
        # 만약 특정 발신 메일만 선택하고 싶다면 'ALL' 대신에 '(FROM "xxxxx@naver.com")' 입력
        status, messages = imap.uid('search', None, 'ALL')
        
        messages = messages[0].split()
        
        # 0이 가장 마지막 메일, -1이 가장 최신 메일
        recent_email = messages[-1]
        
        # fetch 명령어로 메일 가져오기
        res, msg = imap.uid('fetch', recent_email, "(RFC822)")
        
        # 사람이 읽을 수 있는 없는 상태의 이메일
        raw = msg[0][1]
        
        # 사람이 읽을 수 있는 형태로 변환
        raw_readable = msg[0][1].decode('utf-8', errors='ignore')
        
        # print("-------------------")
        # print(raw_readable)
        
        
        # raw_readable에서 원하는 부분만 파싱하기 위해 email 모듈을 이용해 변환
        email_message = email.message_from_string(raw_readable)
        
        # 보낸사람
        fr = make_header(decode_header(email_message.get('From')))
        fr_name, fr_email = parseaddr(email_message.get('From'))
        
        # 메일 제목
        subject = make_header(decode_header(email_message.get('Subject')))
        
        # 메일 내용
        if email_message.is_multipart():
            for part in email_message.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    break
        else:
            body = email_message.get_payload(decode=True)
            
        body = body.decode('utf-8', errors='ignore')
        print(fr)
        print(subject)
        print(body)
        spam_category = self.check_spam(body)
        # DB에 저장
        self.curs.execute("""
            INSERT INTO mail (
                mail_code,
                mail_sender,
                mail_title,
                mail_detail,
                mail_date,
                mail_getter,
                mail_NUM
            ) VALUES (
                send_seq.NEXTVAL,
                :1,
                :2,
                :3,
                SYSDATE,
                'valnet0112@gmail.com',
                :4
            )
        """, (str(fr_email), str(subject), str(body), str(4) if spam_category == 0 else '2'))
        self.conn.commit()

    def __del__(self):
        self.curs.close()
        self.conn.close()

if __name__ == '__main__':
    de = Mygetgmail()
    de.fetch_recent_email()