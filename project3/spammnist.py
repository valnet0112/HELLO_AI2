import email
from email.header import decode_header, make_header
import imaplib
import smtplib
import cx_Oracle
from nltk.stem import PorterStemmer, porter

import numpy as np


# 오라클 DB 연결 설정
oracle_conn = cx_Oracle.connect("TEAM2_202308F", "java", "112.220.114.130:1521/xe")
cursor = oracle_conn.cursor()
# IMAP 서버 연결
imap = imaplib.IMAP4_SSL('imap.gmail.com') #Gmail 메일의 imap 서버의 url 정보를 입력하고 server라는 이름의 변수에 담아줍니다.
smtp = smtplib.SMTP('smtp.gmail.com', 587)

imap.login('valnet0112@gmail.com', 'dofz whgf vrdu hmsj')

imap.select("INBOX")

# 메일 가져와서 Oracle DB에 저장
status, messages = imap.search(None, 'ALL')
messages = messages[0].split()

# 최근 10개 메일 가져오기
recent_emails = messages[-10:]

for message_id in recent_emails:
    _, msg_data = imap.fetch(message_id, '(RFC822)')
    raw_email = msg_data[0][1]
    raw_readable = msg_data[0][1].decode('utf-8')
    email_message = email.message_from_string(raw_readable)

    # 이메일 정보 추출
    fr = make_header(decode_header(email_message.get('From')))
    subject = make_header(decode_header(email_message.get('Subject')))

    # 본문 추출
    if email_message.is_multipart():
        for part in email_message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)
                break
    else:
        body = email_message.get_payload(decode=True)
        
    body = body.decode('utf-8')
    # 본문 전처리
    porter = PorterStemmer()
    word_map = {}
    tempArr = body.split(' ')
    cnt = 0
    for j in range(len(tempArr)):
        tempArr[j] = porter.stem(tempArr[j])

        if tempArr[j] in word_map:
            continue
        else:
            word_map[tempArr[j]] = cnt
            cnt = cnt + 1
    print(word_map)
    exit()        
    # DB에 저장
    cursor.execute("INSERT INTO YOUR_TABLE_NAME (FROM_ADDRESS, SUBJECT, BODY) VALUES (:1, :2, :3)",
                   (str(fr), str(subject), str(body, 'utf-8')))
    oracle_conn.commit()
    
    

# 연결 종료
cursor.close()
oracle_conn.close()
imap.close()
imap.logout()
