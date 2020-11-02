#!/usr/bin/env bash
c_n=`ps aux|grep 'bot.py'|wc -l`

if [ $c_n -eq 1 ]; then
  echo "start graia bot"
  nohup /home/ebi/.conda/envs/mirai20200729/bin/python /home/ebi/Projects/qqbot/setubot/bot.py > /home/ebi/Projects/qqbot/setubot/logs/bot.log 2>&1 &
  exit 0
fi
  echo "graia bot already in running"
  exit 0