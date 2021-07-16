import smtplib 
from email.mime.text import MIMEText
import os
EMAIL='venueyeonnam@gmail.com'  
PASSWORD='yxexkpjdmcqkfedb'
#EMAIL = os.environ['EMAIL']
#PASSWORD = os.environ['PASSWORD']
def send_double_notification_mail(data):
    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 25) 
        smtp.starttls() # TLS 사용시 필요 
        msg_str = data['name'] + '님의 예약이 중복되어 일정을 업로드하지 못했습니다. \n' + '예약 시간: ' + data['start_date'][:-6] + ' ~ ' + data['end_date'][:-6] + ' \n예약 장소는 ' + data['place'] +'이며, ' + data['platform'] + '로 예약했습니다.'
        smtp.login(EMAIL, PASSWORD) 
        msg = MIMEText(msg_str) 
        msg['Subject'] = '베뉴 연남 예약 중복 알림' 
        msg['To'] = EMAIL
        smtp.sendmail(EMAIL, EMAIL, msg.as_string()) 
        smtp.quit()
        print('중복 알림 메일 발송 완료')

    except Exception as e:
        print('중복 알림 메일 발송 실패')