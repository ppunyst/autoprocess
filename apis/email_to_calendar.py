import imaplib
import email
from time import sleep
from email.header import decode_header
import base64
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from apis import calendar_event_add, calendar_event_delete, sheet_add_update, sheet_delete_update, calendar_event_double_check, notion_calendar_event_add, email_notify_double, send_orange_msg
from config import logger

EMAIL='venueyeonnam@gmail.com'  
PASSWORD='yxexkpjdmcqkfedb'
EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASSWORD']
SERVER = 'imap.gmail.com'

def mailsvr():
    latest = ''

    logger.info('Connect To ' + EMAIL + "...")
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")
    logger.info('Connect!')

    #########################
    # fromName
    # 1. naverbooking_noreply@navercorp.com
    # 2. no-reply@hourplace.co.kr
    # 3. office@spacecloud.kr
    ##########################
    #fromName = 'sean.kim.business@gmail.com' or 'jisunpark95@naver.com' or 'naverbooking_noreply@navercorp.com' or 'no-reply@hourplace.co.kr' or 'office@spacecloud.kr' or 'venueyeonnam@gmail.com'
    #fromMail = '{}{}{}'.format('(UNSEEN from ', fromName, ')')
    
    #_, msgnums = mail.search(None, fromMail)
    #email_ids = msgnums[0].split()

    fromName = ['sean.kim.business@gmail.com', 'jisunpark95@naver.com', 'naverbooking_noreply@navercorp.com', 'no-reply@hourplace.co.kr', 'office@spacecloud.kr', 'venueyeonnam@gmail.com']
    email_ids = []
    for name in fromName:
        fromMail = '{}{}{}'.format('(UNSEEN from ', name, ')')
        _, msgnums = mail.search(None, fromMail)
        email_ids += msgnums[0].split()

    print(email_ids)

    if len(email_ids) == 0:
        mail.close()
        return 0, 0

    latest_id = email_ids[-1:][0]

    if latest_id == latest:
        mail.close()
        return 0, 0

    if latest == '': #first
        latest = email_ids[0]
        eachIdsList = email_ids[ email_ids.index(latest) : email_ids.index(latest_id) + 1 ]
    else:
        eachIdsList = email_ids[ email_ids.index(latest) + 1 : email_ids.index(latest_id) + 1 ]
    latest = latest_id

    result = str(len(email_ids))
    logger.info('unseen mail is {}, new unseen mail is {}.'.format(result, len(eachIdsList)))
    
    mails = []
    for e_id in eachIdsList:
        _, data = mail.fetch(e_id, '(RFC822)')
        mails.append(GetContents(data))

    mail.close()
    logger.info('DisConnect!')
    return result, mails

def GetContents(data):
    raw_email = data[0][1]

    raw_email_string = raw_email.decode('utf-8')        
    email_message = email.message_from_string(raw_email_string)
    
    fromWho = email.utils.parseaddr(email_message['From'])[1]
    subject = email_message['Subject']

    if len(subject) != 0:
        subject, encoding = decode_header(subject)[0]
        subject = subject.decode(encoding)
    else:
        subject = '()'
    
     # Contents
    while email_message.is_multipart():
        email_message = email_message.get_payload(0)

    content = email_message.get_payload()
    content = base64.b64decode(content).decode()

    return fromWho, subject, content

def naver_calendar(mail):
    print('***naver***')
    data = {}
    idx = mail[2].find('예약자명')
    idx2 = mail[2].find('예약신청')
    data['name'] = mail[2][idx+4:idx2-2]
    idx = mail[2].find('이용일시')
    idx2 = mail[2].find('결제상태')
    date = mail[2][idx+4:idx2-1]
    data['start_date'] = date[0:4] + '-' + date[5:7] + '-' + date[8:10] + 'T' + date[18:20]+':00:00+09:00'
    data['end_date'] = date[0:4] + '-' + date[5:7] + '-' + date[8:10] + 'T' + date[27:29] +':00:00+09:00'
    idx = mail[2].find('테라스')
    data['place'] = '베뉴 연남' if idx == -1 else '베뉴 연남 더 테라스' 
    return data

def hourplace_calendar(mail):
    print('***hourplace***')
    data = {}
    idx = mail[2].find('게스트 정보')
    idx2 = mail[2].find('직책')
    data['name'] = mail[2][idx+12:idx2-4]
    idx = mail[2].find('촬영 스케줄')
    idx2 = mail[2].find('총 촬영 시간')
    date = mail[2][idx+6:idx2-4]
    data['start_date'] = date[0:4] +'-' + date[6:8] +'-' + date[10:12] + 'T' + date[14:16] + ':00:00+09:00'
    data['end_date'] = date[0:4] +'-' + date[6:8] +'-' + date[10:12] + 'T' + date[-5:-3] +':00:00+09:00' 
    idx = mail[2].find('테라스')
    data['place'] = '베뉴 연남' if idx == -1 else '베뉴 연남 더 테라스'
    return data

def spacecloud_calendar(mail):
    print('***spacecloud***')
    data = {}
    idx = mail[2].find('예약자명')
    data['name'] = mail[2][idx+4:idx+7]
    idx = mail[2].find('예약내용')
    idx2 = mail[2].find('예약인원')
    date = mail[2][idx+4:idx2-1]
    data['start_date'] = date[0:4] + '-' + date[5:7] + '-' + date[8:10] + 'T' + date[11:13] + ':00:00+09:00'
    data['end_date'] = date[0:4] + '-' + date[5:7] + '-' + date[8:10] + 'T' + date[-3:-1] + ':00:00+09:00'
    idx = mail[2].find('테라스')
    data['place'] = '베뉴 연남' if idx == -1 else '베뉴 연남 더 테라스'
    return data

def naver_db(mail, data):
    db_data = {}
    idx = mail[2].find('예약번호')
    idx2 = mail[2].find('예약상품촬영')
    db_data['no'] = mail[2][idx+4:idx2-2]
    db_data['name'] = data['name']
    db_data['phone'] = ''
    db_data['start_date'] = data['start_date']
    db_data['end_date'] = data['end_date']
    idx = mail[2].find('결제수단')
    idx2 = mail[2].find('결제금액촬영')
    db_data['method'] = mail[2][idx+4:idx2-1]
    idx = mail[2].find('=')
    idx2 = mail[2].find('요청사항')
    db_data['amount'] = mail[2][idx+2:idx2-2]
    db_data['platform'] = 'naver'
    db_data['place'] = data['place']
    idx = mail[2].find('결제상태') 
    idx2 = mail[2].find('결제수단')
    db_data['status'] = mail[2][idx+4:idx2-1]
    db_data['id'] = db_data['no'] + db_data['name']
    # db_data['deposit']
    return db_data

def hourplace_db(mail, data):
    db_data = {}
    idx = mail[2].find('예약번호')
    idx2 = mail[2].find('\n', idx)
    db_data['no'] = mail[2][idx+4:idx2].replace(' ', '')
    db_data['name'] = data['name']
    db_data['phone'] = ''
    db_data['start_date'] = data['start_date']
    db_data['end_date'] = data['end_date']
    db_data['method'] = ''
    idx = mail[2].find('총 금액')
    idx2 = mail[2].find('(수수료 제외)')
    db_data['amount'] = mail[2][idx+4:idx2-3]
    db_data['platform'] = 'hourplace'
    db_data['place'] = data['place']
    db_data['status'] = ''
    # db_data['deposit']
    db_data['id'] = db_data['no'] + db_data['name']
    return db_data

def spacecloud_db(mail, data):
    db_data = {}
    db_data['no'] = ''
    db_data['name'] = data['name']
    idx = mail[2].find('전화번호')
    idx2 = mail[2].find('\n', idx)
    db_data['phone'] = mail[2][idx+4:idx2]
    db_data['start_date'] = data['start_date']
    db_data['end_date'] = data['end_date']
    idx = mail[2].find('결제수단')
    idx2 = mail[2].find('\n', idx)
    db_data['method'] = mail[2][idx+4:idx2]
    idx = mail[2].find('결제금액')
    idx2 = mail[2].find('\n', idx)
    db_data['amount'] = mail[2][idx+5:idx2]
    db_data['platform'] = 'spacecloud'
    db_data['place'] = data['place']
    db_data['status'] = ''
    # db_data['deposit']
    db_data['id'] = db_data['phone'] + db_data['name']
    return db_data

def naver_db_update(mail, data):
    db_data = {}
    idx = mail[2].find('예약번호')
    idx2 = mail[2].find('예약상품촬영')
    db_data['no'] = mail[2][idx+4:idx2-2]
    db_data['name'] = data['name']
    db_data['start_date'] = data['start_date']
    db_data['end_date'] = data['end_date']
    db_data['platform'] = 'naver'
    db_data['place'] = data['place']
    idx = mail[2].find('결제상태')
    idx2 = mail[2].find('결제수단')
    db_data['status'] = mail[2][idx+4:idx2-1]
    # db_data['deposit']
    db_data['id'] = db_data['no'] + db_data['name']
    return db_data

def hourplace_db_update(mail, data):
    db_data = {}
    idx = mail[2].find('예약번호')
    idx2 = mail[2].find('\n', idx)
    db_data['no'] = mail[2][idx+4:idx2].replace(' ', '')
    db_data['name'] = data['name']
    db_data['start_date'] = data['start_date']
    db_data['end_date'] = data['end_date']
    db_data['platform'] = 'hourplace'
    db_data['place'] = data['place']
    db_data['status'] = '예약취소'
    # db_data['deposit']
    db_data['id'] = db_data['no'] + db_data['name']
    return db_data

def spacecloud_db_update(mail, data):
    db_data = {}
    db_data['no'] = ''
    db_data['name'] = data['name']
    idx = mail[2].find('전화번호')
    idx2 = mail[2].find('\n', idx)
    db_data['phone'] = mail[2][idx+4:idx2]
    db_data['start_date'] = data['start_date']
    db_data['end_date'] = data['end_date']
    db_data['platform'] = 'spacecloud'
    db_data['place'] = data['place']
    db_data['status'] = '예약취소'
    # db_data['deposit']
    db_data['id'] = db_data['phone'] + db_data['name']
    return db_data

def check_mail():
    while True:
        count, mails = mailsvr()
        if count == 0:
            sleep(10)
            continue
        else:
            #########################
            # Case 총 9개(일단 8개부터)
            # 네이버 샘플 
            # 1. [네이버 예약] 베뉴연남(VenueYeonnam) 새로운 예약이 접수되어 입금대기 중입니다. -> 캘린더 업데이트 O
            # 2. [네이버 예약] 베뉴 연남 고객님이 예약을 취소하셨습니다. -> 캘린더 업데이트 O (취소)
            # 3. [네이버 예약] 베뉴연남(VenueYeonnam) 입금이 완료되어 예약이 확정되었습니다. -> 캘린더 업데이트 O 
            # 4. [네이버 예약] 베뉴 연남 새로운 예약이 확정 되었습니다. -> 캘린더 업데이트 O & 알림톡 O

            # 아워플레이스 샘플
            # 5. [hourplace] 아워플레이스 예약 확정 안내 -> 캘린더 업데이트 O & 알림톡 O
            # 6. [hourplace] 아워플레이스 예약 진행 불가 안내 -> 캘린더 업데이트 O (취소)

            # 스페이스 클라우드 샘플
            # 7. 스페이스 클라우드 예약 완료 메일 -> 캘린더 업데이트 O & 알림톡 O
            # 8. [스페이스클라우드]~ 정산 안내 -> 캘린더 업데이트 X / 세금 관련 정보로 별도의 DB 저장 원함. 
            # 9. 스페이스 클라우드 취소 완료 메일 -> 캘린더 업데이트 O (취소)
            ##########################
            #구글 캘린더 업데이트 

            for mail in mails:
                logger.info(mail)
                if '예약이 확정' in mail[1] or '예약 확정' in mail[1] or '예약 완료' in mail[1]:
                    logger.info('구글 캘린더 업데이트 필요 - 예약 추가')
                    
                    if '네이버' in mail[1]:
                        data = naver_calendar(mail)
                        db_data = naver_db(mail, data)
                        
                    elif 'hourplace' in mail[1]:
                        data = hourplace_calendar(mail)
                        db_data = hourplace_db(mail, data)
        
                    else:
                        data = spacecloud_calendar(mail)                 
                        db_data = spacecloud_db(mail, data)
                    
                    logger.info(db_data)
                    logger.info(data)
                    duplicated = calendar_event_double_check.double_check(data)

                    if not duplicated:
                        calendar_event_add.calendar_add(data)
                        sheet_add_update.sheet_add(db_data)
                        notion_calendar_event_add.notion_calendar_push(data)
                        if db_data['platform'] == 'spacecloud':
                            send_orange_msg.org_msg_send(data['phone'])
                    else:
                        logger.info('중복 notification')
                        email_notify_double.send_double_notification_mail(db_data)

                elif '취소' in mail[1] or '예약 진행 불가' in mail[1]:
                    logger.info('구글 캘린더 업데이트 필요 - 예약 삭제')
                    if '네이버' in mail[1]:
                        data = naver_calendar(mail)
                        db_data = naver_db_update(mail, data)
                    
                    elif 'hourplace' in mail[1]:
                        data = hourplace_calendar(mail)
                        db_data = hourplace_db_update(mail, data)
        
                    else:
                        data = spacecloud_calendar(mail)
                        db_data = spacecloud_db_update(mail, data)
                    
                    logger.info(data)
                    logger.info(db_data)
                    calendar_event_delete.calendar_delete(data)
                    sheet_delete_update.sheet_delete(db_data)

                elif '입금대기' in mail[1]:
                    logger.info('구글 캘린더 업데이트 필요 - 예약 추가 && 입금 대기 상태 DB')
                    data = naver_calendar(mail)
                    db_data = naver_db(mail, data)

                    logger.info(data)
                    logger.info(db_data)
                    duplicated = calendar_event_double_check.double_check(data)
                    if not duplicated:
                        calendar_event_add.calendar_add(data)
                        sheet_add_update.sheet_add(db_data)
                        notion_calendar_event_add.notion_calendar_push(data)
                    else:
                        logger.info('중복 notification')
                        email_notify_double.send_double_notification_mail(db_data)

                elif '정산 안내' in mail[1]:
                    logger.info('세금 관련 별도 DB 저장 필요')

                elif '오렌지' in mail[1]:
                    if mail[2].find('네이버') >= 0:
                        idx = mail[2].find('전화번호:')
                        print(mail[2][idx+6:idx+17])
                        send_orange_msg.org_msg_send(mail[2][idx+6:idx+17])
                    
                    else:
                        idx = mail[2].find('연락처 :')
                        print(mail[2][idx+6:idx+19])
                        send_orange_msg.org_msg_send(mail[2][idx+6:idx+19])
            sleep(10)

# check_mail()



