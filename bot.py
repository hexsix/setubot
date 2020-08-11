# coding: utf-8

""" --------------------------------------
Filename: main.py
Description: bot 主程序
Author: hexsix
Date: 2020/08/10
-------------------------------------- """
import json
import asyncio
import re
# from pathlib import Path

from graia.broadcast import Broadcast
from graia.application.entry import (
    GraiaMiraiApplication, Session,
    MessageChain, FriendMessage, GroupMessage,
    Group, Friend, Member,
    Plain, Image
)

from img import Setu


loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
configs = json.load(open('config.json'))
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=configs['port'],  # 填入 http api 服务运行的地址
        authKey=configs['authKey'],  # 填入 authKey
        account=configs['qq'],  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
setu = Setu('./imgs')


@bcc.receiver(GroupMessage)
async def setu_sender(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    if group.id in configs['allowedGroups']:
        messagestr = message.asDisplay()
        message_list = message.asDisplay().split('，')
        try:
            # setu
            if re.match(r'^小六，涩图，\d，.*', messagestr) or re.match(r'^狼狼，涩图，\d，.*', messagestr):
                n, tags = min(5, int(message_list[2])), message_list[3].split(' ')
                temp_paths = setu.random_imgs(n, tags)
                if temp_paths:
                    for temp_path in temp_paths:
                        await app.sendGroupMessage(group.id, MessageChain.create([Image.fromLocalFile(temp_path)]))
                else:
                    await app.sendGroupMessage(group.id, MessageChain.create([Plain(f'{message_list[3]}: 0')]))
            elif re.match(r'^小六，涩图，\d', messagestr) or re.match(r'^狼狼，涩图，\d', messagestr):
                n, tags = min(5, int(message_list[2])), []
                for temp_path in setu.random_imgs(n, tags):
                    await app.sendGroupMessage(group.id, MessageChain.create([Image.fromLocalFile(temp_path)]))
            elif re.match(r'^小六，涩图', messagestr) or re.match(r'^狼狼，涩图', messagestr) or re.match(
                    r'^\[At::target=1256500776]\s', messagestr):
                n, tags = 1, []
                for temp_path in setu.random_imgs(n, tags):
                    await app.sendGroupMessage(group.id, MessageChain.create([Image.fromLocalFile(temp_path)]))
            # new setu
            elif re.match(r'^小六，新涩图，\d，.*', messagestr) or re.match(r'^狼狼，新涩图，\d，.*', messagestr):
                n, tags = min(5, int(message_list[2])), message_list[3].split(' ')
                temp_paths = setu.newest_imgs(n, tags)
                if temp_paths:
                    for temp_path in temp_paths:
                        await app.sendGroupMessage(group.id, MessageChain.create([Image.fromLocalFile(temp_path)]))
                else:
                    await app.sendGroupMessage(group.id, MessageChain.create([Plain(f'{message_list[3]}: 0')]))
            elif re.match(r'^小六，新涩图，\d', messagestr) or re.match(r'^狼狼，新涩图，\d', messagestr):
                n, tags = min(5, int(message_list[2])), []
                for temp_path in setu.newest_imgs(n, tags):
                    await app.sendGroupMessage(group.id, MessageChain.create([Image.fromLocalFile(temp_path)]))
            elif re.match(r'^小六，新涩图', messagestr) or re.match(r'^狼狼，新涩图', messagestr):
                n, tags = 3, []
                for temp_path in setu.newest_imgs(n, tags):
                    await app.sendGroupMessage(group.id, MessageChain.create([Image.fromLocalFile(temp_path)]))
            # upload
            elif re.match(r'^小六，\[图片].*', messagestr) or re.match(r'^狼狼，\[图片].*', messagestr):
                img_s_ = message.get(Image)
                try:
                    flag = True
                    if type(img_s_) is list:
                        for img in img_s_:
                            flag &= setu.save_img(img, member.id)
                    else:
                        flag &= setu.save_img(img_s_, member.id)
                    await app.sendGroupMessage(group.id, MessageChain.create([
                        Plain('successfully saved'),
                    ]))
                except:
                    await app.sendGroupMessage(group.id, MessageChain.create([
                        Plain('save failed'),
                    ]))
            # help
            elif re.match(r'^小六，help', messagestr) or re.match(r'^狼狼，help', messagestr):
                await app.sendGroupMessage(group.id, MessageChain.create([Plain(text='under construction')]))

            elif re.match(r'^小六，.*', messagestr) or re.match(r'^狼狼，.*', messagestr):
                await app.sendGroupMessage(group.id, MessageChain.create([Plain(text='zzZ')]))

            else:
                # print(messagestr)
                pass
        except Exception as e:
            await app.sendGroupMessage(group.id, MessageChain.create([Plain(str(e))]))


@bcc.receiver(FriendMessage)
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    # await app.sendFriendMessage(friend, MessageChain.create([
    #     Image.fromLocalFile(setu.random_imgs(n=1, tags=[])[0])
    # ]))
    pass


if __name__ == '__main__':
    app.launch_blocking()
