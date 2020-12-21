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

from config import configs
from utils import save_list, read_list, salt, resize


class ImgYande(object):
    def __init__(self):
        pass

    @staticmethod
    def get_temp_path(img_path: str, idx: int) -> str:
        suffix = img_path.split('.')[-1]
        return os.path.join(configs['temp_imgs'], '.temp_{}.{}'.format(idx, suffix))

    def save_to_temp(self, src_path: str, idx: int) -> str:
        img = cv2.imread(src_path)
        img = resize(img, os.path.getsize(src_path))
        salt_img = salt(img)
        temp_path = self.get_temp_path(src_path, idx)
        cv2.imwrite(temp_path, salt_img)
        return temp_path

    def new_imgs(self) -> Iterator[Tuple[str]]:
        sent_list = read_list(configs['sent_list'])
        error_list = read_list(configs['error_list'])
        filenames = os.listdir(configs['img_dir'])
        while len(sent_list) > 10 + 5 * len(filenames):
            sent_list.popleft()
        for i, filename in enumerate(filenames):
            if filename.endswith('json') or not filename.startswith('yande')\
                    or filename in sent_list or filename in error_list:
                continue
            filepath = os.path.join(configs['img_dir'], filename)
            metadata = json.load(open(f'{filepath}.json', 'r'))
            try:
                temp_img_path = self.save_to_temp(filepath, i)
            except Exception:
                error_list.append(filename)
                save_list(error_list, configs['error_list'])
                print(f'Error while sending {filename}')
                continue
            yield temp_img_path, metadata['source'] if metadata['source'] != '' else metadata['website']
            sent_list.append(filename)
            save_list(sent_list, configs['sent_list'])


if __name__ == '__main__':
    y = ImgYande()
    for item in y.new_imgs():
        print(item)
