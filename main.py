# coding: utf-8

""" --------------------------------------
Filename: main.py
Description: bot 主程序
Author: hexsix
Date: 2020/07/29
-------------------------------------- """
import json

from mirai import Mirai, Plain, MessageChain, Friend, Image, GroupMessage, Group, Member, FriendMessage

from setu import random_setu, newest_setu, save_link_img, save_img
from img import Setu

config = json.load(open('config.json'))
qq = config['qq']  # 字段 qq 的值
authKey = config['authKey']  # 字段 authKey 的值
mirai_api_http_locate = config['port']  # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.
allowed_groups = config['allowedGroups']
call = config['call']

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")
se = Setu()


@app.receiver(GroupMessage)
async def GMHandler(app: Mirai, group: Group, member: Member, message: GroupMessage):
    if group.id in allowed_groups:
        message_list = message.toString().split('，')
        appellation = message_list[0]
        if appellation in call:
            try:
                operation = message_list[1]
                if operation == 'help':
                    await app.sendGroupMessage(group.id, [
                        Plain(text=str(call) + "，涩图[，n]：setu库里随机n张，默认1张，最多5张\n"),
                        Plain(text=str(call) + "，新涩图[，n]：setu库里最新n张，默认3张，最多5张\n"),
                        Plain(text=str(call) + "，{img}：向setu库里添加n张"),
                    ])
                elif operation == '涩图':
                    n, tags = 0, []
                    try:
                        n = min(5, int(message_list[2]))
                    except IndexError:
                        n = 1
                    except ValueError:
                        await app.sendGroupMessage(group.id, [
                            Plain(text='zzZ'),
                        ])
                    try:
                        tags = message_list[3].split(' ')
                    except IndexError:
                        tags = []
                    for temp_img_path in se.random_imgs(n, tags):
                        await app.sendGroupMessage(group.id, [
                            Image.fromFileSystem(temp_img_path),
                        ])
                elif operation == '新涩图':
                    n, tags = 0, []
                    try:
                        n = min(5, int(message_list[2]))
                    except IndexError:
                        n = 3
                    except ValueError:
                        await app.sendGroupMessage(group.id, [
                            Plain(text='zzZ'),
                        ])
                    try:
                        tags = message_list[3].split(' ')
                    except IndexError:
                        tags = []
                    for temp_img_path in se.newest_imgs(n, tags):
                        await app.sendGroupMessage(group.id, [
                            Image.fromFileSystem(temp_img_path),
                        ])
                elif operation[:4] == 'http':
                    await app.sendGroupMessage(group.id, [
                        Plain(text=save_link_img(message.toString()[3:])),
                    ])
                elif operation[:6] == '[Image':
                    img_s_ = message.messageChain.getAllofComponent(Image)
                    try:
                        flag = True
                        if type(img_s_) is list:
                            for img in img_s_:
                                flag &= save_img(img)
                        else:
                            flag &= save_img(img_s_)
                        await app.sendGroupMessage(group.id, [
                            Plain(text='保存成功'),
                        ])
                    except:
                        await app.sendGroupMessage(group.id, [
                            Plain(text='zzZ'),
                        ])
                else:
                    await app.sendGroupMessage(group.id, [
                        Plain(text='zzZ'),
                    ])
            except IndexError:
                await app.sendGroupMessage(group.id, [
                    Plain(text="zzZ"),
                ])


if __name__ == "__main__":
    app.run()
