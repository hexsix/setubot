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
import traceback
# from pathlib import Path
from datetime import datetime

from graia.broadcast import Broadcast
from graia.application.entry import (
    GraiaMiraiApplication, Session,
    MessageChain, FriendMessage, GroupMessage,
    Group, Friend, Member,
    Plain, Image
)
from graia.application.context import enter_context

from img import Setu, Img


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
                n, tags = min(5, int(message_list[2])), message_list[3:]
                count = 0
                for temp_path, filename, tags, source in setu.random_imgs(n, tags):
                    count += 1
                    await app.sendGroupMessage(group.id, MessageChain.create(
                        [Plain(f'source:{source}\ntags:{tags}\n'), Image.fromLocalFile(temp_path)]))
                if count != n:
                    await app.sendGroupMessage(group.id, MessageChain.create([Plain(f'{message_list[3:]}: {count}')]))
            elif re.match(r'^小六，涩图，\d', messagestr) or re.match(r'^狼狼，涩图，\d', messagestr):
                n, tags = min(5, int(message_list[2])), []
                for temp_path, filename, tags, source in setu.random_imgs(n, tags):
                    await app.sendGroupMessage(group.id, MessageChain.create(
                        [Plain(f'source:{source}\ntags:{tags}\n'), Image.fromLocalFile(temp_path)]))
            elif re.match(r'^小六，涩图', messagestr) or re.match(r'^狼狼，涩图', messagestr):
                n, tags = 1, []
                for temp_path, filename, tags, source in setu.random_imgs(n, tags):
                    await app.sendGroupMessage(group.id, MessageChain.create(
                        [Plain(f'source:{source}\ntags:{tags}\n'), Image.fromLocalFile(temp_path)]))
            # help
            elif re.match(r'^小六，help', messagestr) or re.match(r'^狼狼，help', messagestr):
                await app.sendGroupMessage(group.id, MessageChain.create([Plain(text='小六，涩图[，n[，tag0[，tag1...]]]')]))

            elif re.match(r'^小六，.*', messagestr) or re.match(r'^狼狼，.*', messagestr):
                await app.sendGroupMessage(group.id, MessageChain.create([Plain(text='zzZ')]))

            else:
                # print(messagestr)
                pass
        except Exception as e:
            await app.sendGroupMessage(group.id, MessageChain.create([Plain(str(e))]))
            traceback.print_exc()


@bcc.receiver(FriendMessage)
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    # await app.sendFriendMessage(friend, MessageChain.create([
    #     Image.fromLocalFile(setu.random_imgs(n=1, tags=[])[0])
    # ]))
    pass


sended_imgs = set()


async def zhengdiansetu():
    global sended_imgs
    while True:
        await asyncio.sleep(1)
        if datetime.now().minute == 0 and datetime.now().second == 0 and datetime.now().hour in range(18, 24):
            for temp_path, annotation, tags, source in setu.yande_popular(5, sended_imgs):
                with enter_context(app=app, event_i=zhengdiansetu):
                    await app.sendGroupMessage(configs['allowedGroups'][0], MessageChain.create(
                        [Plain(f'yande.re popular\nsource:{source}\ntags:{tags}\n'), Image.fromLocalFile(temp_path)]))
                    await app.sendGroupMessage(configs['allowedGroups'][1], MessageChain.create(
                        [Plain(f'yande.re popular\nsource:{source}\ntags:{tags}\n'), Image.fromLocalFile(temp_path)]))
        if datetime.now().second == 0:
            for temp_path, annotation, tags, source in setu.new_imgs(5, sended_imgs):
                with enter_context(app=app, event_i=zhengdiansetu):
                    await app.sendGroupMessage(configs['allowedGroups'][0], MessageChain.create(
                        [Plain(f'Pickup\nannotation:{annotation}\nsource:{source}\ntags:{tags}\n'),
                         Image.fromLocalFile(temp_path)]))
        if datetime.now().minute == 59 and datetime.now().second == 59 and datetime.now().hour == 23:
            for temp_path, annotation, tags, source in setu.yande_popular(12, sended_imgs):
                with enter_context(app=app, event_i=zhengdiansetu):
                    await app.sendGroupMessage(configs['allowedGroups'][0], MessageChain.create(
                        [Plain(f'yande.re popular\nsource:{source}\ntags:{tags}\n'), Image.fromLocalFile(temp_path)]))
                    await app.sendGroupMessage(configs['allowedGroups'][1], MessageChain.create(
                        [Plain(f'yande.re popular\nsource:{source}\ntags:{tags}\n'), Image.fromLocalFile(temp_path)]))
        if datetime.now().hour == 8 and datetime.now().minute == 0 and datetime.now().second == 0:
            sended_imgs.clear()
        # if datetime.now().second % 10 == 0 and datetime.now().hour in range(14, 24):
        #     for temp_path, filename, tags, source in setu.new_imgs(1, sended_imgs):
        #         with enter_context(app=app, event_i=zhengdiansetu):
        #             await app.sendGroupMessage(configs['allowedGroups'][2], MessageChain.create(
        #                [Plain(f'filename:{filename}\nSource:{source}\ntags:{tags}'), Image.fromLocalFile(temp_path)]))


if __name__ == '__main__':
    loop.create_task(zhengdiansetu())
    app.launch_blocking()
