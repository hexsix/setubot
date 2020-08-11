# coding: utf-8

""" --------------------------------------
Filename: img.py
Description: 图片处理模块
Author: hexsix
Date: 2020/08/03
-------------------------------------- """

import datetime
import os
import random
from typing import List

import cv2
import numpy as np
import requests


class Img(object):
    def __init__(self, root_dir: str = r'./imgs'):
        self.root_dir = root_dir

    def get_temp_path(self, img_path: str, idx: int) -> str:
        suffix = img_path.split('.')[-1]
        return os.path.join(self.root_dir, '.temp_{}.{}'.format(idx, 'jpg' if suffix == 'jfif' else suffix))

    @staticmethod
    def get_mtime(file_path: str) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

    @staticmethod
    def get_img_paths(root_dir) -> List[str]:
        """
        获得根目录下所有文件路径
        :return: List[文件路径]
        """
        img_paths = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            filenames = [f for f in filenames if not f[0] == '.']       # ignore hidden files
            dirnames[:] = [d for d in dirnames if not d[0] == '.']      # and hidden dirs
            for filename in filenames:
                if filename == 'README.md':
                    continue
                file_path = os.path.join(dirpath, filename)
                img_paths.append(file_path)
        return img_paths

    def sort_paths_by_mtime(self, paths: List[str]) -> List[str]:
        """
        按照修改时间排序
        :param paths: List[文件路径]
        :return: 排好序的 List[文件路径]
        """
        paths_with_mtime = []
        for path in paths:
            mtime = self.get_mtime(path)
            paths_with_mtime.append((path, mtime))
        paths_with_mtime.sort(key=lambda item: item[1], reverse=True)
        return [item[0] for item in paths_with_mtime]

    @staticmethod
    def filter_paths_by_tags(paths: List[str], tags: List[str]) -> List[str]:
        """
        按照 tags 过滤图片路径
        :param paths: List[图片路径]
        :param tags: List[tag]
        :return: 过滤后的 List[图片路径]
        """
        if not tags:
            return paths

        def tags_all_in_path(_path):
            for tag in tags:
                if tag not in _path:
                    return False
            return True

        return [path for path in paths if tags_all_in_path(path)]

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

    def random_imgs(self, n: int, tags: List[str], root_dir: str = r'./imgs') -> List[str]:
        """
        随机图片，返回 temp 图的保存路径
        :param n: 图片数
        :param tags: 标签
        :param root_dir:
        :return: List[图片路径]
        """
        temp_paths = []
        img_paths = self.filter_paths_by_tags(self.get_img_paths(root_dir), tags)
        indexes = random.sample(range(len(img_paths)), min(len(img_paths), n))
        random_img_paths = [img_paths[i] for i in indexes]
        for i, random_img_path in enumerate(random_img_paths):
            temp_paths.append(self.save_to_temp(random_img_path, i))
        return temp_paths

    def newest_imgs(self, n: int, tags: List[str], root_dir: str = r'./imgs') -> List[str]:
        """
        懒了
        :param n:
        :param tags:
        :param root_dir:
        :return:
        """
        temp_paths = []
        img_paths = self.sort_paths_by_mtime(self.filter_paths_by_tags(self.get_img_paths(root_dir), tags))[:n]
        for i, img_path in enumerate(img_paths):
            temp_paths.append(self.save_to_temp(img_path, i))
        return temp_paths

    @staticmethod
    def save_img(img, memberid: int) -> bool:
        """
        保存图片到本地
        :param img:
        :param memberid:
        :return:
        """
        # print(img.url, memberid)
        if not os.path.exists(os.path.join('./imgs/hso/share', str(memberid))):
            os.mkdir(os.path.join('./imgs/hso/share', str(memberid)))
        save_path = os.path.join('./imgs/hso/share', str(memberid), f'qq {memberid} {datetime.datetime.now()}.jpeg')
        try:
            img = requests.get(img.url).content
            with open(save_path, 'wb') as f:
                f.write(img)
            return True
        except Exception:
            return False


class Setu(Img):
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
    print(Img().newest_imgs(5, []))
    pass
