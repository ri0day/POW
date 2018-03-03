##### 介绍
- `aliyunsms_v2.py` 短信报警实现-阿里云
- `twilio_sms_call.py`  语音报警实现(支持 tts)-twilio

#####使用
1. `pip install -r requirements.txt`
2. 阿里云通道的需要修改access key,access secret,sign,模版信息,twilio的通道需要修改拨出电话号码,token,sid
3. `python aliyunsms_v2.py 15802170000 '{"your_template_key":"your_template_value"}'`
4. `python twilio_sms_call.py 15802170000 'msg'`
