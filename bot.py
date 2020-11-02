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
from datetime import datetime

from graia.broadcast import Broadcast
from graia.application.entry import (
    GraiaMiraiApplication, Session,
    MessageChain, FriendMessage, GroupMessage,
    Group, Friend, Member,
    Plain, Image
)
from graia.application.context import enter_context

from yande_re_popular_imgs import ImgYande
from eagle_imgs import ImgEagle


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


@bcc.receiver(GroupMessage)
async def setu_sender(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    if group.id in configs['allowedGroups']:
        setu = ImgEagle()
        messagestr = message.asDisplay()
        message_list = message.asDisplay().split('，')
        try:
            # setu
            count, n, tags = 0, 0, []
            if re.match(r'^狼狼，涩图，\d，.*', messagestr):
                n, tags = min(5, int(message_list[2])), message_list[3:]
            elif re.match(r'^狼狼，涩图，\d$', messagestr):
                n = min(5, int(message_list[2]))
            elif re.match(r'^狼狼，涩图，.*', messagestr):
                n, tags = 1, message_list[2:]
            elif re.match(r'^狼狼，涩图$', messagestr):
                n = 1
            # help
            elif re.match(r'^狼狼，help$', messagestr):
                await app.sendGroupMessage(group.id, MessageChain.create([Plain(text="""狼狼，涩图：随机发送一张涩图
狼狼，涩图，n：随机发送n张涩图
狼狼，涩图，tags，...：随机发送一张包含tags的涩图
狼狼，涩图，n，tags，...：随机发送n张包含tags的涩图
狼狼，help：本消息
n为非个位数时会报错，且最多发送5张图
tags为完全匹配
注意是中文逗号""")]))
            # zzZ
            elif re.match(r'^狼狼，.*', messagestr):
                await app.sendGroupMessage(group.id, MessageChain.create([Plain(text='zzZ')]))

            for temp_path, source in setu.random_imgs(n, tags):
                count += 1
                await app.sendGroupMessage(group.id, MessageChain.create([Plain(source), Image.fromLocalFile(temp_path)]))
            if count != n:
                await app.sendGroupMessage(group.id, MessageChain.create([Plain(f'{tags}: {count}')]))
        except Exception as e:
            await app.sendGroupMessage(group.id, MessageChain.create([Plain(str(e))]))
            traceback.print_exc()


@bcc.receiver(FriendMessage)
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    # await app.sendFriendMessage(friend, MessageChain.create([
    #     Image.fromLocalFile(setu.random_imgs(n=1, tags=[])[0])
    # ]))
    pass


async def zhengdiansetu():
    while True:
        await asyncio.sleep(1)
        if datetime.now().second == 0:
            img_yande = ImgYande()
            try:
                for temp_path, source in img_yande.new_imgs():
                    with enter_context(app=app, event_i=zhengdiansetu):
                        for i in range(0, 3):
                            await app.sendGroupMessage(configs['allowedGroups'][i], MessageChain.create([Plain(source), Image.fromLocalFile(temp_path)]))
            except Exception as e:
                await app.sendGroupMessage(configs['allowedGroups'][3], MessageChain.create([Plain(str(e))]))
                traceback.print_exc()


if __name__ == '__main__':
    loop.create_task(zhengdiansetu())
    app.launch_blocking()
