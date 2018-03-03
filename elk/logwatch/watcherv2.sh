#!/bin/bash
echo "--------START PROCESS at $(date +%Y.%m.%d-%H:%M:%S)------"

cd /opt/logwatcher
index_file=/opt/logwatcher/idxv2.list
output_file=/tmp/x.log
endpoint="http://elk-vnode01:9200/_cat/indices"

gen_idx_list() {
time=$1
echo "fetch index list ,time: $time "
curl -s $endpoint|awk  "/$time/ {print \$3}"|grep -vE "(msd|winlogbeat|nginx|filebeat|fanba|management|logstash-$time|debug|payment|tradeprocess)"   >$index_file
if grep -q $time $index_file
then
    echo "[genindex function] index  file generated"
else
    echo "[genindex function]: can't find index"
fi
}

Search() {
:>$output_file
if [ -s "$index_file" ]
then
  for index in $(cat $index_file)
    do
      python logwatcher.py $index >>$output_file
    done
else
  echo "[Search function]: no index found"
fi
}

SendNotification() {
if [ -s "$output_file" ]
then
    if grep -q ERROR $output_file
      then
       echo 'in sending notification'
       sh senderv2.sh
    else
      echo "[send function]: no result,exit"
    fi
else
    echo "[send function]: output file empty,exit"
fi

}


dt=$(date +%Y.%m.%d)
gen_idx_list $dt 
Search
r=$(SendNotification)

echo $r

if [ $(date +%H) -le 08 ]
then
    if [[ "$r" =~ 'exit' ]]
    then
      echo "in retry function....."
      dt=$(date -d '-1days' +%Y.%m.%d)
      gen_idx_list $dt 
      Search
      SendNotification
    else
      echo "notification function status: $r"
    fi
else
  echo "not 0-08 no retry"
fi

echo "--------END PROCESS at $(date +%Y.%m.%d-%H:%M:%S)------"
