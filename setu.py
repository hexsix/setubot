# coding: utf-8

""" --------------------------------------
Filename: setu.py
Description: RT
Author: hexsix
Date: 2020/07/29
-------------------------------------- """
import datetime
import os
import time
from random import randint
from typing import List, Tuple

import cv2
import numpy as np
import requests

setu_dir = r'./imgs/hso'


def get_sorted_setu_paths() -> List[Tuple[str, datetime.datetime]]:
    """
    遍历 setu 文件夹，返回按照修改时间排序的 setu，新的在前
    :return: List[Tuple[setu_path, modified_time]]
    """
    ret = []
    for path, _, file_list in os.walk(setu_dir):
        for file_name in file_list:
            if file_name[0] == '.':
                continue        # ignore hidden files
            file_path = os.path.join(path, file_name)
            modified_time = time.localtime(os.stat(file_path).st_mtime)
            y = time.strftime('%Y', modified_time)
            m = time.strftime('%m', modified_time)
            d = time.strftime('%d', modified_time)
            H = time.strftime('%H', modified_time)
            M = time.strftime('%M', modified_time)
            then = datetime.datetime(int(y), int(m), int(d), int(H), int(M))
            ret.append((file_path, then))
    ret.sort(key=lambda item: item[1], reverse=True)
    return ret


def get_temp_path(img_path):
    suffix = '.' + img_path.split('.')[-1]
    if suffix == '.jfif':
        suffix = '.jpg'        # twitter jfif is jpg, cv2 recgonize jpg
    ret = r'./imgs/temp' + suffix
    return ret


def random_setu() -> str:
    """
    从 setu 文件夹中随机抽取一张 setu，撒盐，保存到 temp.jpg/temp.png
    :return: temp.jpg/temp.png
    """
    setu_list = get_sorted_setu_paths()
    idx = randint(0, len(setu_list) - 1)
    setu_path = setu_list[idx][0]
    setu = cv2.imread(setu_path)
    salty_setu = salt(setu)
    temp_path = get_temp_path(setu_path)
    cv2.imwrite(temp_path, salty_setu)
    return temp_path


def newest_setu(n: int = 3) -> List[str]:
    """
    从 setu 文件夹中返回最新的 n 张椒盐 setu
    :param n: RT
    :return: RT
    """
    setu_paths = [item[0] for item in get_sorted_setu_paths()[:n]]
    for setu_path in setu_paths:
        setu = cv2.imread(setu_path)
        salty_setu = salt(setu)
        temp_path = get_temp_path(setu_path)
        cv2.imwrite(temp_path, salty_setu)
        yield temp_path


def salt(img: np.ndarray, n: int = 6) -> np.ndarray:
    """
    椒盐setu
    :param img: img mat
    :param n: number of salt
    :return: salty img mat
    """
    for k in range(n):
        i = randint(0, img.shape[1] - 1)
        j = randint(0, img.shape[0] - 1)
        if img.ndim == 2:
            img[j, i] = 255
        elif img.ndim == 3:
            img[j, i, 0] = randint(0, 255)
            img[j, i, 1] = randint(0, 255)
            img[j, i, 2] = randint(0, 255)
    return img


def save_link_img(link: str) -> str:
    suffix = link.split('.')[-1]
    if suffix in ['png', 'PNG', 'jpg', 'jpeg', 'JPG', 'JPEG', 'jfif', 'JFIF']:
        save_path = './imgs/hso/share/' + str(datetime.datetime.now()) + '.' + suffix
        try:
            img = requests.get(link, proxies={"http": "localhost:7890", "https": "localhost:7890"}).content
            with open(save_path, 'wb') as f:
                f.write(img)
            return '保存成功'
        except Exception as e:
            return str(e)
    else:
        return '小六现在没法处理尾缀不是JPG/PNG的链接。'


def save_img(img) -> str:
    save_path = './imgs/hso/share/' + str(datetime.datetime.now()) + '.jpeg'
    try:
        img = requests.get(img.url).content
        with open(save_path, 'wb') as f:
            f.write(img)
        return '保存成功'
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    pass
