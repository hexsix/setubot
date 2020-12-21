""" --------------------------------------
Filename: main.py
Description: bot 主程序
Author: hexsix
Date: 2020/08/10
-------------------------------------- """
import asyncio
import traceback
from datetime import datetime

from graia.broadcast import Broadcast
from graia.application.entry import (
    GraiaMiraiApplication, Session,
    MessageChain,
    Group, Member,
    Plain, Image
)
from graia.application.context import enter_context

from yande_re_popular_imgs import ImgYande
from yandedl import yande_dl
from config import configs


loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=configs['port'],  # 填入 http api 服务运行的地址
        authKey=configs['authKey'],  # 填入 authKey
        account=configs['qq'],  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)


async def auto_yande_dl():
    while 1:
        await asyncio.sleep(30)
        if datetime.now().minute == 58:
            try:
                with enter_context(app, auto_yande_dl):
                    await app.sendGroupMessage(configs['allowedGroups'][0], MessageChain.create([
                        Plain(yande_dl())
                    ]))
            except Exception:
                await app.sendGroupMessage(configs['allowedGroups'][0], MessageChain.create([
                    Plain(str(traceback.format_exc()))
                ]))


async def auto_send_popular():
    while 1:
        await asyncio.sleep(59)

        try:
            img = ImgYande()
            for temp_path, source in img.new_imgs():
                with enter_context(app=app, event_i=auto_send_popular):
                    for group_id in configs['allowedGroups'][1:]:
                        await app.sendGroupMessage(group_id, MessageChain.create([
                            Plain(source), Image.fromLocalFile(temp_path)
                        ]))
        except Exception:
            await app.sendGroupMessage(configs['allowedGroups'][0], MessageChain.create([
                Plain(str(traceback.format_exc()))
            ]))


@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    if group.id != configs['allowedGroups'][0] and member.id:
        return
    if message.asDisplay().startswith("dl reboot"):
        loop.create_task(auto_yande_dl())
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("ok")
        ]))
    if message.asDisplay().startswith("send reboot"):
        loop.create_task(auto_send_popular())
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("ok")
        ]))


if __name__ == '__main__':
    loop.create_task(auto_yande_dl())
    loop.create_task(auto_send_popular())
    app.launch_blocking()
