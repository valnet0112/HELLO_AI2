import email
from email.header import decode_header, make_header
import imaplib
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

# Gmail 계정 정보
email_address = 'your_email@gmail.com'
password = 'your_password'

# IMAP 서버 연결
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_address, password)
mail.select('inbox')  # 다른 메일함을 사용하려면 여기에 해당 메일함 이름을 입력하세요.

# SQLite 데이터베이스 연결
engine = create_engine('sqlite:///mails.db')
metadata = MetaData()

# 메일함 테이블 정의
mails_table = Table('mails', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('from_address', String),
                   Column('subject', String),
                   Column('body', String)
                   )
metadata.create_all(engine)

# 메일 가져와서 데이터베이스에 저장
status, messages = mail.search(None, 'ALL')
messages = messages[0].split()

for message_id in messages:
    _, msg_data = mail.fetch(message_id, '(RFC822)')
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # 이메일 정보 추출
    from_address = make_header(decode_header(email_message.get('From')))
    subject = make_header(decode_header(email_message.get('Subject')))

    # 본문 추출
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                break
    else:
        body = email_message.get_payload(decode=True)

    # 데이터베이스에 저장
    conn = engine.connect()
    conn.execute(mails_table.insert().values(
        from_address=str(from_address),
        subject=str(subject),
        body=str(body, 'utf-8')
    ))
    conn.close()

# IMAP 연결 종료
mail.close()
mail.logout()
