# coding: utf-8

""" --------------------------------------
Filename: eagle_imgs.py
Description: 图片处理模块 for eagle
Author: hexsix
Date: 2020/08/03
-------------------------------------- """

import os
import json
import random
import datetime
from collections import deque
from typing import List

import cv2

from utils import save_list, read_list, salt, resize


class ImgEagle(object):
    def __init__(self):
        self.root_dir = r'/home/ebi/Projects/Pictures'
        self.img_dir = os.path.join(self.root_dir, "Eagle/illustration.library/images")
        self.images = {}
        self.tags = {}

    def init_images(self):
        ignore_tags = {'game screenshot', 'meme', 'interesting', 'ignore'}
        for dirpath, dirnames, filenames in os.walk(self.img_dir):
            for filename in filenames:
                if filename == 'metadata.json':
                    metadata = json.load(open(os.path.join(dirpath, filename)))
                    if len(ignore_tags & set(metadata['tags'])) > 0:
                        continue
                    self.images[metadata['id']] = metadata

    def init_tags(self):
        for (img_id, metadata) in self.images.items():
            if not metadata['tags']:
                continue
            for tag in metadata['tags']:
                try:
                    self.tags[tag].add(img_id)
                except:
                    self.tags[tag] = {img_id}

    def get_temp_path(self, img_path: str, idx: int) -> str:
        suffix = img_path.split('.')[-1]
        return os.path.join(self.root_dir, 'temp_imgs/.temp_{}.{}'.format(idx, 'jpg' if suffix == 'jfif' else suffix))

    def save_to_temp(self, src_path: str, idx: int) -> str:
        img = cv2.imread(src_path)
        img = resize(img, os.path.getsize(src_path))
        salt_img = salt(img)
        temp_path = self.get_temp_path(src_path, idx)
        cv2.imwrite(temp_path, salt_img)
        return temp_path

    def random_imgs(self, n, tags: List[str]):
        if n == 0: return []
        sended_random = list(read_list(os.path.join(self.root_dir, 'sended_random.txt')))
        life = float(sended_random[0])
        if datetime.datetime.now().timestamp() - life > 1200:
            sended_random = set()
        else:
            sended_random = set(sended_random[1:])

        self.init_images()
        self.init_tags()
        img_ids = self.images.keys() - sended_random
        try:
            for tag in tags:
                img_ids = img_ids & self.tags[tag]
        except:
            return []

        indexes = random.sample(range(len(img_ids)), min(len(img_ids), n))
        random_img_ids = [list(img_ids)[i] for i in indexes]

        for i, img_id in enumerate(random_img_ids):
            sended_random.add(img_id)
            filename = f'{self.images[img_id]["name"]}.{self.images[img_id]["ext"]}'
            filepath = os.path.join(self.img_dir, f'{img_id}.info/{filename}')
            temppath = self.save_to_temp(filepath, i)
            yield temppath, self.images[img_id]["url"]
        sended_random = deque(sended_random)
        sended_random.appendleft(datetime.datetime.now().timestamp())
        save_list(sended_random, os.path.join(self.root_dir, 'sended_random.txt'))
