##### 介绍
logwatche从es里面搜索指定关键字,发现关键字触发邮件报警.

#### 组件
- logwatcher.py 查询es脚本,关键字定义
- watcherv2.sh 程序入口,负责生成要查询的index列表.然后触发搜索
- senderv2.sh 告警入口.
- mail.py 邮件发送程序

