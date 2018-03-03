#!/bin/bash
now=$(date)
fivemin=$(date -d '- 5min')
to="devsalert@abc.com"
from="opsalert@abc.com"
file="/tmp/x.log"

send(){
if [ -f $file ]
then
  if [[ $1 == "attach" ]]
    then
      python mail.py -s mail.abc.com -f $from -t  $to -u opsalert -p 'passwd' -S "Log Alert from PROD  from $fivemin to $now" -m "Please Check the Attachment x.log" -F $file 
    elif [[ $1 == "body" ]]
      then
      python mail.py -s mail.abc.com -f $from -t  $to -u opsalert -p 'passwd' -S "Log Alert from PROD from $fivemin to $now" -m "$(cat $file|iconv -f gbk -t UTF-8)"
    else
      echo "method not supported"
  fi
else
echo "result file not fond,exit"
fi
}


filesize=$(du -s $file|awk '{print $1}')
oversize=124

if [ "$filesize" -gt "$oversize" ]
then
  echo "overlimit send by attach"
  send attach
else
  echo "send by messages in body"
  send body
fi
