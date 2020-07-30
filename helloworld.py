import base64
import datetime
import time
import json

from mirai import Mirai, Plain, MessageChain, Friend, Image, GroupMessage, Group, Member, FriendMessage
import asyncio
import os
import random
from random import randint
import cv2

config = json.load(open('config.json'))
qq = config['qq']  # 字段 qq 的值
authKey = config['authKey']  # 字段 authKey 的值
mirai_api_http_locate = config['port']  # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.
allowed_groups = config['allowedGroups']

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")


# @app.receiver("FriendMessage")
# async def event_gm(app: Mirai, friend: Friend):
#
#     await app.sendFriendMessage(friend, [
#         Plain(text="色图\n"),
#         Image.fromFileSystem('imgs/yellow.jpg'),
#     ])


def get_img_path():
    img_list = []
    g = os.walk("./imgs/hso")
    for path, d, filelist in g:
        for filename in filelist:
            file_path = os.path.join(path, filename)
            img_list.append(file_path)
    img_list_length = len(img_list)
    idx = random.randint(0, img_list_length - 1)
    return img_list[idx]


def get_new_img_path():
    now = datetime.datetime.now()
    new_img_list = []
    g = os.walk("./imgs/hso")
    for path, d, filelist in g:
        for filename in filelist:
            if filename == '.stignore':
                continue
            file_path = os.path.join(path, filename)
            ModifiedTime = time.localtime(os.stat(file_path).st_mtime)
            y = time.strftime('%Y', ModifiedTime)
            m = time.strftime('%m', ModifiedTime)
            d = time.strftime('%d', ModifiedTime)
            H = time.strftime('%H', ModifiedTime)
            M = time.strftime('%M', ModifiedTime)
            d2 = datetime.datetime(int(y), int(m), int(d), int(H), int(M))
            if now - d2 < datetime.timedelta(days=1):
                new_img_list.append((file_path, d2))
    # img_list_length = len(new_img_list)
    # idx = random.randint(0, img_list_length - 1)
    new_img_list.sort(key=lambda item: item[1], reverse=True)
    return [item[0] for item in new_img_list[:3]]


def cv2_base64(img, img_type):
    if img_type == '.jfif':
        img_type = '.jpg'
    base64_str = cv2.imencode(img_type, img)[1]
    base64_str = str(base64.b64encode(base64_str)[2:-1])
    return base64_str


def salt(img, n=3):
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


def get_temp_path(img_path):
    zzz = img_path.split('.')
    houzhui = '.' + zzz[-1]
    if houzhui == '.jfif':
        houzhui = '.jpg'
    ret = r'./imgs/temp' + houzhui
    return ret


@app.receiver(FriendMessage)
async def FMHandler(app: Mirai, friend: Friend, message: FriendMessage):
    if message.toString() == '小六，涩图':
        img_path = get_img_path()
        temp_path = get_temp_path(img_path)
        img = cv2.imread(img_path)
        cv2.imwrite(temp_path, img)
        await app.sendFriendMessage(friend, [
            Image.fromFileSystem(temp_path),
        ])
    print(message.json())
    print(message.toString())
    pass


@app.receiver(GroupMessage)
async def GMHandler(app: Mirai, group: Group, member: Member, message: GroupMessage):
    if group.id in allowed_groups:
        if message.toString() == '小六，涩图':
            img_path = get_img_path()
            temp_path = get_temp_path(img_path)
            img = cv2.imread(img_path)
            img = salt(img)
            # base64str = cv2_base64(img, '.' + img_path.split('.')[-1])
            cv2.imwrite(temp_path, img)
            await app.sendGroupMessage(group, [
                Image.fromFileSystem(temp_path),
            ])
        elif message.toString() == '小六，新涩图':
            img_paths = get_new_img_path()
            if not img_paths:
                await app.sendGroupMessage(group, [
                    Plain(text='小六今天没更新涩图'),
                ])
            for img_path in img_paths:
                temp_path = get_temp_path(img_path)
                img = cv2.imread(img_path)
                img = salt(img)
                cv2.imwrite(temp_path, img)
                await app.sendGroupMessage(group, [
                    Image.fromFileSystem(temp_path),
                ])
    pass


if __name__ == "__main__":
    app.run()
