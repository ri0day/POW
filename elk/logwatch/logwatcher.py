#coding: utf-8
from elasticsearch import Elasticsearch
import time,sys  

#ES_URL = 'http://10.117.82.4:9200'
ES_URL = 'http://10.46.67.46:9200'

now = int(round(time.time() * 1000))
fivemin = int(now - (300*1000)) 


es = Elasticsearch(ES_URL)
time_range = {
              "range": {
                "@timestamp": {
                  "gte": fivemin,
                  "lte": now,
                  "format": "epoch_millis"
                }
              }
}

q = {
  "query": { 
    "bool": { 
      "must": [
        time_range,
        { "match": { "message":   "ERROR"        }}  
      ],

     "must_not" : [
       { "match": { "message":   "spent"        }},
       { "match": { "message":   "Spent"        }},
       { "match": { "message":   "Spend"        }},
       { "match": { "message":   "INFO"        }},
       { "match": { "message":   "调用金核卡bin查询接口失败"        }},
       { "match_phrase" : {"message": "Madison.Product.Service.ProductServerManager - update product_001 ProductBidManager status error" }},
       { "match_phrase" : {"message": "Madison.ServiceCenter.MQ.QueueProcessor - Network work error, renew memcache object" }},
       { "match_phrase" : {"message": "Madison.ExternalRelated.Service.WeChatServer"}},
       { "match_phrase" : {"message": "Madison.TangApp3._0.LooYuService.ReceiveMsgFromLooYuServices" }},
       { "match_phrase" : {"message": "ERROR Madison.Activities.Service.Activity.MidasTouchManager - Current account points not enough"}},
       { "match_phrase" : {"message": "ERROR Madison.Client.API.Request.Activity.HundredGroup.CreateGroupRequest" }},
       { "match_phrase" : {"message": "ERROR Madison.Product.Service.AccountBalanceToDemandjob - AccountBalanceToDemand" }},
       { "match_phrase" : {"message": "error InsertStoreProfitHistoryDetail accountID"}},
       { "match_phrase" : {"message": "Deadlock found when trying to get lock"}},
       { "match_phrase" : {"message": "金额必须为正数" }},
       { "match_phrase" : {"message": "ILLEGAL_ARGUMENT" }},
       { "match_phrase" : {"message": "您的登录态发生异常" }},
       { "match_phrase" : {"message": "集合已修改；可能无法执行枚举操作" }},
       { "match_phrase" : {"message": "账户余额超限" }},
       { "match_phrase" : {"message": "解绑银行卡" }},
       { "match_phrase" : {"message": "给乐语在线客服发送消息发生异常,详细信息:System.Net.WebException: 操作超时" }},
       { "match_phrase" : {"message": "给乐语在线客服发送消息发生异常,详细信息:System.Net.WebException: The operation has timed out" }},
       { "match_phrase" : {"message": "用户积分不够" }},
       { "match_phrase" : {"message": "生成订单号失败" }},
       { "match_phrase" : {"message": "基础资产存续期状态更新异常" }},
       { "match_phrase" : {"message": "分享至朋友圈可获得一次补签的机会，当周仅限补签一天，本周已有分享补签记录" }},
       { "match_phrase" : {"message": "Midas Touch activity has not started or has ended already" }},
       { "match_phrase" : {"message": "ERROR Madison.Client.API.Request.Activity.Baihe.BaiheGateWay2Request - baihe timestamp is out of date" }},
       { "match_phrase" : {"message": "ERROR Madison.Client.API.Request.Activity.MidasTouch.MidasTouchAwardHistoryRequest - Midas Touch activity has not started or has ended already" }},
       { "match_phrase" : {"message": "商品兑换人数太多" }},
       { "match_phrase" : {"message": "您的唐果不足" }},
       { "match_phrase" : {"message": "购买失败撤销使用加息券失败"}},
       { "match_phrase" : {"message": "根据类型获取AppBanner出错了"}},
       { "match_phrase" : {"message": "TradeBusinessException" }},
       { "match_phrase" : {"message": "每日累计充值不能超过" }},
       { "match_phrase" : {"message": "您已经兑换过该档位奖品" }},
       { "match_phrase" : {"message": "register err" }},
       { "match_phrase" : {"message": "third union login is" }},
       { "match_phrase" : {"message": "Madison.Client.API.Request.Activity.HundredGroup.CanBuyProductToJoinRequest" }},
       { "match_phrase" : {"message": "baihe mobile is empty," }},
       { "match_phrase" : {"message": "MidNightActivityService - midNight activity investDuration error" }},
       { "match_phrase" : {"message": "SubStanceRewardReceive Error" }},
       { "match_phrase" : {"message": "ERROR NETUserService - Decode accountId error in queryUserInfo. AccountId" }},
       { "match_phrase" : {"message": "ProductServerManager还剩可购投资金额" }},
       { "match_phrase" : {"message": "Madison.Activities.Service.Activity.MidasTouchManager - Midas Touch activity investment -add or update Midas Touch points failed" }},
       { "match_phrase" : {"message": "ERROR AesUtils - decrypt error  java.lang.IllegalArgumentException: Null input buffer" }},
       { "match_phrase" : {"message": "ERROR Madison.Activities.Service.Job.StoreThousandActivitiesJob - StoreThousandActivitiesJob" }},
       { "match_phrase" : {"message": "ERROR CatInterceptor - exception message =null java.lang.reflect.InvocationTargetException: null" }},
       { "match_phrase" : {"message": "http://ad.baihe.com/Txs/record" }},
       { "match_phrase" : {"message": "百合爱情账户接口访问失败" }},
       { "match_phrase" : {"message": "org.springframework.web.HttpRequestMethodNotSupportedException:" }},
       { "match_phrase" : {"message": "multiple of 16"}},
       { "match_phrase" : {"message": "No mapping for the Unicode character exists in the target multi-byte code page"}},
       { "match_phrase" : {"message": "Wechat h5 dynamic CORS has exception"}},
       { "match_phrase" : {"message": "TOKEN 未找到"}},
       { "match_phrase" : {"message": "0元白拿活动奖品兑换"}},
       { "match_phrase" : {"message": "不处于0元白拿活动时间"}},
       { "match_phrase" : {"message": "QueryFinanceCoreP2PAssetsException"}},
       { "match_phrase" : {"message": "NewInviteNormal RewardsSendChangeSaleTypeFixed"}},
       { "match_phrase" : {"message": "NewInviteNormalRewards_InsertNew"}},
       { "match_phrase" : {"message": "Madison.JobCenter.JobDispatcher - Job execution error"}},
       { "match_phrase" : {"message": "The remote server returned an error: (500) Internal Server Error"}},
       { "match_phrase" : {"message": "StoredProcedure NewInviteNormalRewards_InsertNew"}},
       { "match_phrase" : {"message": "ERROR Madison.Client.API.Request.Activity.MidasTouch.MidasTouchDrawLotteryRequest" }}
 ]
  }
  }
}

print "===================Process %s:=========================="%sys.argv[1]
d = es.search(body=q, index=sys.argv[1])

for line in  d['hits']['hits']:
    print line['_source']['message'].encode('gbk')
