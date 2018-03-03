#!/usr/bin/python
#coding: utf-8
import os,logging
from uuid import uuid4
from twilio.rest import TwilioRestClient
from twilio.exceptions import TwilioRestException
from urllib import urlencode
import sys
account_sid = "account sid"
auth_token = "token"

logging.basicConfig(format='%(asctime)s %(message)s',filename='alert.log', level=logging.INFO)

#templates mapping
templates={'chinese':'https://handler.twilio.com/twiml/EH212d790b628a6be7d183619c510eca5d','en':'https://handler.twilio.com/twiml/EHee3038f5a029cf705eb11db9ae76757e' ,'play':'https://handler.twilio.com/twiml/EH8815a556bdef8d11929dbe0c1c14187c'}

class VoiceAlert(object):
    def __init__(self ,tw_from, msg_type, msg):
        self.sid = os.getenv('TWILIO_SID',account_sid)
        self.token = os.getenv('TWILIO_TOKEN',auth_token)
        self.client = TwilioRestClient(self.sid, self.token)
        self.msg_type = msg_type
        self.msg = msg
        self.uuid = uuid4()
        self.tw_from = tw_from

    def url_builder(self):
        tail = urlencode({'msg':self.msg})
        url = templates.get(self.msg_type)+'''?&%s'''%tail
        self.url = url
        return url

    def make_call(self,to):
         self.url_builder()
         try:
             call = self.client.calls.create(to=to, from_=self.tw_from, url=self.url)
             logging.info('uuid:%s making call to %s ,sid:%s'%(self.uuid, to,call.sid))
         except TwilioRestException as e:
             logging.info(e)
    def send_sms(self,to):
         try:
             sms = self.client.messages.create(to=to,from_=self.tw_from,body=self.msg)
             logging.info('uuid:%s send sms to %s ,sid:%s'%(self.uuid, to, sms.sid))
         except TwilioRestException as e:
             logging.info(e)

msg=sys.argv[2]
mob = '+86'+sys.argv[1]

alert = VoiceAlert(tw_from='+14804283769',msg_type='play',msg=msg)
alert.send_sms(to=mob)
alert.make_call(to=mob)
