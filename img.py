# coding: utf-8

""" --------------------------------------
Filename: img.py
Description: 图片处理模块
Author: hexsix
Date: 2020/08/03
-------------------------------------- """

import os
import json
import random
import datetime
from typing import List, Dict, Set

import cv2
import numpy as np


class Img(object):
    @staticmethod
    def init_images_dict():
        images = {}
        for dirpath, dirnames, filenames in os.walk('./Eagle/illustration.library/images'):
            for filename in filenames:
                if filename == 'metadata.json':
                    j = json.load(open(os.path.join(dirpath, filename)))
                    if 'game screenshot' in j['tags'] or 'meme' in j['tags'] or 'interesting' in j['tags']:
                        continue
                    images[j['id']] = j
        return images

    @staticmethod
    def init_tags_dict(images) -> Dict[str, Set[str]]:
        tags = {}
        for (k, v) in images.items():
            if v['tags']:
                for tag in v['tags']:
                    try:
                        tags[tag].add(k)
                    except:
                        tags[tag] = {k}
        return tags

    def __init__(self, root_dir: str = r'./imgs'):
        self.root_dir = root_dir

    def get_temp_path(self, img_path: str, idx: int) -> str:
        suffix = img_path.split('.')[-1]
        return os.path.join(self.root_dir, '.temp_{}.{}'.format(idx, 'jpg' if suffix == 'jfif' else suffix))

    def save_to_temp(self, src_path: str, idx: int) -> str:
        """
        保存图片到 temp.png/jpg
        :param src_path: 原图路径
        :param idx: 0 ~ 4，最多发 5 张图
        :return: 新图位置
        """
        img = cv2.imread(src_path)
        temp_path = self.get_temp_path(src_path, idx)
        cv2.imwrite(temp_path, img)
        return temp_path

    def random_imgs(self, n: int, tags: List[str]) -> List[str]:
        """
        随机图片，返回 temp 图的保存路径
        :param n: 图片数
        :param tags: 标签
        :return:
        """
        images_dict = self.init_images_dict()
        tags_dict = self.init_tags_dict(images_dict)
        imgid_set = images_dict.keys()
        for tag in tags:
            if tag in tags_dict:
                imgid_set = imgid_set & tags_dict[tag]
            else:
                return []

        indexes = random.sample(range(len(imgid_set)), min(len(imgid_set), n))
        imgid_list = list(imgid_set)
        random_imgid_list = [imgid_list[i] for i in indexes]

        for i, imgid in enumerate(random_imgid_list):
            img_path = os.path.join('./Eagle/illustration.library/images', f'{imgid}.info',
                                    f'{images_dict[imgid]["name"]}.{images_dict[imgid]["ext"]}')
            temp_img_path = self.save_to_temp(img_path, i)

            indexes = random.sample(range(len(images_dict[imgid]["tags"])), min(len(images_dict[imgid]["tags"]), 5))
            random_tags_list = [images_dict[imgid]["tags"][i] for i in indexes]

            yield temp_img_path, images_dict[imgid]["annotation"][:10], random_tags_list, images_dict[imgid]["url"]

    def new_imgs(self, n, sended_imgs):
        """
        每日新图
        :param n: int
        :return:
        """
        now = int(datetime.datetime.now().timestamp())
        images_dict = self.init_images_dict()
        imgid_set = set()
        for k, v in images_dict.items():
            if now - 5 * 60 * 60 < int(str(v['btime'])[:-3]) and v['id'] not in sended_imgs and 'pickup' in v['tags']:
                imgid_set.add(k)

        imgid_set = imgid_set - sended_imgs
        imgid_list = list(imgid_set)
        indexes = random.sample(range(len(imgid_list)), min(len(imgid_list), n))
        random_imgid_list = [imgid_list[i] for i in indexes]

        for i, imgid in enumerate(random_imgid_list):
            sended_imgs.add(imgid)
            img_path = os.path.join('./Eagle/illustration.library/images', f'{imgid}.info',
                                    f'{images_dict[imgid]["name"]}.{images_dict[imgid]["ext"]}')
            temp_img_path = self.save_to_temp(img_path, i)

            indexes = random.sample(range(len(images_dict[imgid]["tags"])), min(len(images_dict[imgid]["tags"]), 5))
            random_tags_list = [images_dict[imgid]["tags"][i] for i in indexes]

            yield temp_img_path, images_dict[imgid]["annotation"], random_tags_list, images_dict[imgid]["url"]

    def yande_popular(self, n, sended_imgs):
        """
        yande popular
        :param n:
        :param sended_imgs:
        :return:
        """
        now = int(datetime.datetime.now().timestamp())
        images_dict = self.init_images_dict()
        imgid_set = set()
        for k, v in images_dict.items():
            if now - 24 * 60 * 60 < int(str(v['btime'])[:-3]) and v['id'] not in sended_imgs and 'yande' in v['tags']:
                imgid_set.add(k)

        imgid_set = imgid_set - sended_imgs
        imgid_list = list(imgid_set)
        indexes = random.sample(range(len(imgid_list)), min(len(imgid_list), n))
        random_imgid_list = [imgid_list[i] for i in indexes]

        for i, imgid in enumerate(random_imgid_list):
            sended_imgs.add(imgid)
            img_path = os.path.join('./Eagle/illustration.library/images', f'{imgid}.info',
                                    f'{images_dict[imgid]["name"]}.{images_dict[imgid]["ext"]}')
            temp_img_path = self.save_to_temp(img_path, i)

            indexes = random.sample(range(len(images_dict[imgid]["tags"])), min(len(images_dict[imgid]["tags"]), 5))
            random_tags_list = [images_dict[imgid]["tags"][i] for i in indexes]

            yield temp_img_path, images_dict[imgid]["annotation"], random_tags_list, images_dict[imgid]["url"]


class Setu(Img):
    @staticmethod
    def init_images_dict():
        images = {}
        for dirpath, dirnames, filenames in os.walk('./Eagle/illustration.library/images'):
            for filename in filenames:
                if filename == 'metadata.json':
                    j = json.load(open(os.path.join(dirpath, filename)))
                    if 'ignore' in j['tags']:
                        continue
                    images[j['id']] = j
        return images

    @staticmethod
    def salt(img: np.ndarray, n: int = 6) -> np.ndarray:
        """
        椒盐setu
        :param img: img mat
        :param n: number of salt
        :return: salty img mat
        """
        for k in range(n):
            i = random.randint(0, img.shape[1] - 1)
            j = random.randint(0, img.shape[0] - 1)
            if img.ndim == 2:
                img[j, i] = 255
            elif img.ndim == 3:
                img[j, i, 0] = random.randint(0, 255)
                img[j, i, 1] = random.randint(0, 255)
                img[j, i, 2] = random.randint(0, 255)
        return img

    def save_to_temp(self, src_path: str, idx: int) -> str:
        """
        对于setu，需要椒盐保存，保存图片到 temp.png/jpg
        :param src_path: 原图路径
        :param idx: 0 ~ 4，最多发 5 张图
        :return: 新图位置
        """
        img = cv2.imread(src_path)
        salt_img = self.salt(img)
        temp_path = self.get_temp_path(src_path, idx)
        cv2.imwrite(temp_path, salt_img)
        return temp_path


if __name__ == '__main__':
    pass
