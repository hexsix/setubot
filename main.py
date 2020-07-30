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

config = json.load(open('config.json'))
qq = config['qq']  # 字段 qq 的值
authKey = config['authKey']  # 字段 authKey 的值
mirai_api_http_locate = config['port']  # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.
allowed_groups = config['allowedGroups']

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")


@app.receiver(GroupMessage)
async def GMHandler(app: Mirai, group: Group, member: Member, message: GroupMessage):
    if group.id in allowed_groups:
        if message.toString() == '小六，涩图':
            await app.sendGroupMessage(group, [
                Image.fromFileSystem(random_setu()),
            ])
        elif message.toString() == '小六，新涩图':
            for temp_path in newest_setu():
                await app.sendGroupMessage(group, [
                    Image.fromFileSystem(temp_path),
                ])
        elif message.toString()[:3] == '小六，' and message.toString()[3:7] == 'http':
            await app.sendGroupMessage(group, [
                Plain(text=save_link_img(message.toString()[3:])),
            ])
        elif message.toString()[:9] == '小六，[Image':
            await app.sendGroupMessage(group, [
                Plain(text=save_img(message.messageChain.getFirstComponent(Image))),
            ])


if __name__ == "__main__":
    app.run()
