import requests
import json
import time

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config import logger

def org_msg_send(phone):
    try:
        res = requests.post(
                "https://www.apiorange.com/api/send/notice.do",
                headers = {
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': '4NiVJP8Nrh0rVvkB8K64jRh/zfde0AeD7JwcsIZ9dYA=', 
                        },
                data = json.dumps({     
                    'tmp_number': 14688,
                    'kakao_sender': '01029241261',
                    'kakao_phone' : phone, #'01045701543',
                })            
            )
        logger.info(res)
        time.sleep(3)


        res = requests.post(
                "https://www.apiorange.com/api/send/notice.do",
                headers = {
                            'Content-Type': 'application/json; charset=utf-8',
                            'Authorization': '4NiVJP8Nrh0rVvkB8K64jRh/zfde0AeD7JwcsIZ9dYA=', 
                        },
                data = json.dumps({     
                    'tmp_number': 14685,
                    'kakao_sender': '01029241261',
                    'kakao_phone' : phone, #'01045701543',
                })            
            )
        logger.info(res)
        logger.info('오렌지 메세지 알림톡 발송 성공')
    
    except:
        logger.error('오렌지 메세지 발송 실패')