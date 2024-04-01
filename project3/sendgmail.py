import smtplib
from email.mime.text import MIMEText

smtp = smtplib.SMTP('smtp.gmail.com', 587)

smtp.ehlo()

smtp.starttls()

smtp.login('valnet0112@gmail.com', 'dofz whgf vrdu hmsj')

msg = MIMEText('내용 : 스팸메일 필터링을 할 것이다')
msg['Subject'] = '제목: 파이썬으로 gmail 보내기'

smtp.sendmail('valnet0112@gmail.com', 'valnet0112@gmail.com', msg.as_string())

smtp.quit()