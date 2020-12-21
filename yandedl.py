""" --------------------------------------
Filename: yandedl.py
Description: yande.re popular download
Author: hexsix
Date: 2020/12/21
-------------------------------------- """
import os
import traceback
import urllib.parse
import re
import json
from typing import Iterator

import feedparser
import requests.utils

from config import configs
from utils import save_list, read_list


def validate_filename(filename: str) -> str:
    return re.sub(r'[/\\:*?"<>|]', "_", filename)  # 替换为下划线


def parse(j: dict) -> Iterator[tuple]:
    saved_list = read_list(configs['saved_list'])
    while len(saved_list) > 100:
        saved_list.popleft()
    for entry in j['entries']:
        post_url = entry['link']
        img_id = post_url.split('/')[-1]
        if img_id in saved_list:
            continue
        score = int(re.search(r'Score:\d*', entry['content'][0]['value']).group().split(':')[-1])
        if score < 40:
            continue
        origin_url = entry['links'][1]['href']
        origin_type = entry['links'][1]['type'].split('/')[1]
        source = ''
        try:
            source = re.search(r'href="[^"]*', entry['content'][0]['value']).group().split('"')[1]
            source = urllib.parse.unquote(source)
            source = 'https://www.pixiv.net/artworks/' + re.search(r'\d*_p\d', source).group().split('_')[0]
        except:
            pass
        tags = [item['term'] for item in entry['tags']]
        img_filename = 'yande.re {}.{}'.format(img_id, origin_type)
        img_filename = validate_filename(img_filename)
        yield img_id, post_url, origin_url, source, img_filename, tags


def img_download(img_id, post_url, origin_url, source, img_filename, tags):
    saved_list = read_list(configs['saved_list'])

    html = requests.Session().get(origin_url)
    with open(os.path.join(configs['img_dir'], img_filename), 'wb') as f:
        f.write(html.content)

    json.dump({
        "url": urllib.parse.unquote(origin_url),
        "name": img_filename,
        "website": urllib.parse.unquote(post_url),
        "tags": tags,
        "source": urllib.parse.unquote(source)
    }, open(os.path.join(configs['img_dir'], f'{img_filename}.json'), 'w'))

    saved_list.append(img_id)
    save_list(saved_list, configs['saved_list'])


def yande_dl() -> str:
    success, fail = 0, 0

    try:
        j = feedparser.parse(configs['rss_url'])
        for items in parse(j):
            try:
                img_download(*items)
                success += 1
            except Exception:
                fail += 1
                continue
    except Exception:
        return traceback.format_exc()

    return f"{success} 张图保存成功\t{fail} 张图保存失败"


if __name__ == '__main__':
    pass
