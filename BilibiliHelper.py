import asyncio
import aiofiles
import queue
from bilibili_api import live, sync
from OpenaiHelper import OpenaiHelper
import time
import re
from time import sleep
import openai
from colorama import init, Back, Fore
class BilibiliHelper:
    def __init__(self,config):
        self.config = config
        self.user_message_pool=queue.Queue()
        self.response_pool=queue.Queue()
        self.openai_helper = OpenaiHelper(config)
        # self.terminal_set = True
    def run(self):
        init(autoreset=True)
        loop = asyncio.get_event_loop()
        loop.create_task(self.connect())
        loop.create_task(self.processing_massage())
        loop.create_task(self.show_response())
        loop.run_forever()
        # asyncio.run(self.processing_massage())
    # def get_terminal_setting(self):
    #     self.terminal_set = not self.terminal_set
    #     if self.terminal_set:
    #         return Back.BLUE,Fore.WHITE
    #     else :
    #         return Back.WHITE,Fore.BLACK
        
    async def connect(self):
        room = live.LiveDanmaku(self.config['roomid'])
        @room.on('DANMU_MSG')
        async def on_danmaku(event):
            # 收到完散定时器
            # print(event)
            self.user_message_pool.put({
                'user':event['data']['info'][2][1],
                'message':event['data']['info'][1],
            })
        
        await room.connect() 
    async def processing_massage(self):
        while True:
            if not self.user_message_pool.empty():
                user_message = self.user_message_pool.get()
                msg = user_message['message']
                # print(msg)
                msg=re.sub("：",":",msg)
                matches = re.findall(r'(?<=c:)[^ ]+',msg)
                if len(matches)>0:
                    try :
                        respond = await self.openai_helper.get_chat_response(message=matches[0])
                        # print(respond)
                        self.response_pool.put({
                            'user':user_message['user'],
                            'message':matches[0],
                            'respond':respond,
                        })
                    except Exception as e:
                        print(e)
            await asyncio.sleep(1)
        ##message = self.user_massage_pool.get()['massage']
        ##return self.openai_helper.get_response(message=message)
    async def show_response(self):
        while True:
            if not self.response_pool.empty():
                try:
                    response = self.response_pool.get()
                    print(f"{response['user']} 主人好啊~\n")
                    print(f"主人的问题是:{response['message']}")
                    print(f"{response['respond']}")
                    print("-------------------------")
                except Exception as e:
                        print(e)
            await asyncio.sleep(1)
                # async with aiofiles.open('./response.md','a+',encoding='utf-8') as f:
                    # await f.write('---\n\n')
                    # await f.write(f"{response['user']}主人好啊~\n\n")
                    # await f.write(f"主人的问题是:{response['message']}\n\n")
                    # await f.write(f"{response['respond']}\n\n\n")
            