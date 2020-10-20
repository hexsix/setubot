# coding: utf-8

""" --------------------------------------
Filename: yande_re_popular_imgs.py
Description: 图片处理模块 for yande popular
Author: hexsix
Date: 2020/10/19
-------------------------------------- """

import os
import json
from typing import Iterator, Tuple

import cv2

from utils import save_list, read_list, salt


class ImgYande(object):
    def __init__(self):
        self.root_dir = r'/home/ebi/Projects/miraiok/python195bot/'
        self.img_dir = os.path.join(self.root_dir, 'yandedl/yande_popular')

    def get_temp_path(self, img_path: str, idx: int) -> str:
        suffix = img_path.split('.')[-1]
        return os.path.join(self.root_dir, 'temp_imgs/.temp_{}.{}'.format(idx, 'jpg' if suffix == 'jfif' else suffix))

    def save_to_temp(self, src_path: str, idx: int) -> str:
        img = cv2.imread(src_path)
        salt_img = salt(img)
        temp_path = self.get_temp_path(src_path, idx)
        cv2.imwrite(temp_path, salt_img)
        return temp_path

    def new_imgs(self) -> Iterator[Tuple[str]]:
        sended_popular = read_list(os.path.join(self.root_dir, 'sended_popular.txt'))
        filenames = os.listdir(os.path.join(self.root_dir, 'yandedl/yande_popular'))
        while len(sended_popular) > 5 * len(filenames):
            sended_popular.popleft()
        for i, filename in enumerate(filenames):
            if filename.endswith('json') or not filename.startswith('yande') or filename in sended_popular:
                continue
            sended_popular.append(filename)
            filepath = os.path.join(self.root_dir, 'yandedl/yande_popular', filename)
            metadata = json.load(open(f'{filepath}.json', 'r'))
            temp_img_path = self.save_to_temp(filepath, i)
            yield temp_img_path, metadata['source'] if metadata['source'] != '' else metadata['website']
        save_list(sended_popular, os.path.join(self.root_dir, 'sended_popular.txt'))


if __name__ == '__main__':
    y = ImgYande()
    for item in y.new_imgs():
        print(item)
    pass
