#!/bin/bash

while true
do
    procnum=` ps -ef|grep "yanderss.py"|grep -v grep|wc -l`
   if [ $procnum -eq 0 ]; then
       nohup /home/ebi/.conda/envs/mirai20200729/bin/python /home/ebi/Projects/miraiok/python195bot/yandedl/yanderss.py &
   fi
   sleep 20
done
