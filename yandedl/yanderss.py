# coding: utf-8

""" ----------------------------
filename: yanderss.py
description: 下载 yande.re popular 1d
author: hexsix
date: 2020/9/10
---------------------------- """

from collections import deque
import datetime
import json
import logging
import os
import time
import traceback
import sched
from typing import Tuple

import requests
from lxml import etree


ROOT_DIR = r'/home/ebi/Projects/miraiok/python195bot/yandedl'


def save_list(arr: deque, filename: str):
    with open(filename, 'w', encoding='utf8') as f:
        for item in arr:
            f.write(f'{item}\n')


def read_list(filename: str) -> deque:
    return deque([item.strip() for item in open(filename, 'r', encoding='utf8').readlines()])


def rss_page_analysis(html: str) -> Tuple[str]:
    saved_list = read_list(os.path.join(ROOT_DIR, 'secret/saved_list.txt'))
    while len(saved_list) > 100:
        saved_list.popleft()
    content = etree.HTML(html.encode())
    for entry in content.xpath('//entry'):
        post_url = entry.xpath('link/@href')[0]
        img_id = post_url.split('/')[-1]
        if img_id in saved_list:
            continue
        origin_url = entry.xpath('link/@href')[1]
        cdata_dom = etree.HTML(etree.tostring(entry.xpath('content')[0], encoding="UTF-8").decode())
        source = cdata_dom.xpath('//a/@href')
        tags = entry.xpath('category/@term')
        score = int([p for p in cdata_dom.xpath('//p/text()') if p[:5] == 'Score'][0].split(':')[1])
        if score < 40:
            continue
        saved_list.append(img_id)
        img_filename = requests.utils.unquote(origin_url).split('/')[-1]
        if source:
            yield img_id, post_url, origin_url, source[0], img_filename, tags
        else:
            yield img_id, post_url, origin_url, '', img_filename, tags
    save_list(saved_list, os.path.join(ROOT_DIR, 'secret/saved_list.txt'))


def init_session(filename: str) -> requests.Session:
    session = requests.Session()
    proxy = {"http": "127.0.0.1:8889", "https": "127.0.0.1:8889"}
    rss_headers = json.load(open(filename, 'r', encoding='utf8'))
    session.proxies = proxy
    session.headers = rss_headers
    return session


def yande_download(img_id, post_url, origin_url, source, img_filename, tags):
    yande_session = init_session(os.path.join(ROOT_DIR, 'secret/yande_headers.json'))

    html = yande_session.get(origin_url)
    with open(os.path.join(ROOT_DIR, 'yande_popular', img_filename), 'wb') as f:
        f.write(html.content)

    json.dump({
        "url": origin_url,
        "name": img_filename,
        "website": post_url,
        "tags": tags + ['yande_popular'],
        "source": source
    }, open(os.path.join(ROOT_DIR, 'yande_popular', f'{img_filename}.json'), 'w'))

    yande_session.close()


def main():
    rss_session = init_session(os.path.join(ROOT_DIR, 'secret/rss_headers.json'))

    rss_url = open(os.path.join(ROOT_DIR, 'secret/rss_url.txt'), 'r', encoding='utf8').readlines()[0].strip()
    success, fail = 0, 0
    try:
        html = rss_session.get(rss_url).text
        for items in rss_page_analysis(html):
            try:
                yande_download(*items)
                success += 1
            except Exception:
                fail += 1
                logging.log(level=logging.ERROR, msg=traceback.format_exc())
                print(traceback.format_exc())
                continue
    except Exception:
        logging.log(level=logging.ERROR, msg=traceback.format_exc())
        print(traceback.format_exc())
        exit(1)
    finally:
        logging.log(level=logging.INFO, msg=f"{success} 张图保存成功\t{fail} 张图保存失败")
        print(f"{success} 张图保存成功\t{fail} 张图保存失败")

    rss_session.close()


def perform_task():
    scheduler.enter(60 * 60, 0, perform_task)
    main()
    _sched_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    logging.log(level=logging.INFO, msg=f"下次运行在：{_sched_time}")
    print(f"下次运行在：{_sched_time}")


if __name__ == '__main__':
    logging.basicConfig(filename=os.path.join(ROOT_DIR, 'logs/yanderss.log'), level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    main()
    scheduler = sched.scheduler(time.time, time.sleep)
    now = datetime.datetime.now()
    if now.minute < 50:
        sched_time = datetime.datetime(now.year, now.month, now.day, now.hour, 58, 0)
    else:
        sched_time = datetime.datetime(now.year, now.month, now.day, now.hour + 1, 58, 0)
    if sched_time < now:
        sched_time = sched_time.replace(hour=now.hour + 1)
    logging.log(level=logging.INFO, msg=f"下次运行在：{sched_time}")
    print(f"下次运行在：{sched_time}")
    scheduler.enterabs(sched_time.timestamp(), 0, perform_task)  # datetime.timestamp()是python3.3后才有
    scheduler.run()

