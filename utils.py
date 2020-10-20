# coding: utf-8

""" --------------------------------------
Filename: utils.py
Description: 抽一些通用方法出来
Author: hexsix
Date: 2020/10/20
-------------------------------------- """

import random
from collections import deque

import numpy as np


def save_list(arr: deque, filename: str):
    with open(filename, 'w', encoding='utf8') as f:
        for item in arr:
            f.write(f'{item}\n')


def read_list(filename: str) -> deque:
    return deque([item.strip() for item in open(filename, 'r', encoding='utf8').readlines()])


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
