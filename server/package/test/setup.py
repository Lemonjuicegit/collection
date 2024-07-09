# -*- coding: utf-8 -*-
import random
import asyncio
import pandas as pd
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse


def stream(request: Request):
    def new_count():
        return random.randint(1, 100)
    async def event_generator():
        index = 0
        while True:
            index += 1
            if await request.is_disconnected():
                break
            # 测试取随机数据，每次取一个随机数
            if count := new_count():
                yield {'data': count}

            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())

def 改编码(datapath):
    df = pd.read_excel(datapath)
    


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)