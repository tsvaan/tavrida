#!/usr/bin/python3
# coding=utf-8
__author__ = 'Vasily.A.Tsilko'
# Python 3.5+
# Simple test client for tcp_server.py

import asyncio
import datetime
import random

ADDRESS = ("localhost", 8888)
LOOPS = 100  # How many times will be send data string



async def tcp_client():
    data = {"command":8,}
    for x in range(1, 65):
        data["input" + str(x)] = 0 if (x % 2) != 0 else 1 
    for x in range(1, 4):
        data["reserved" + str(x)] = x + -123.4
    
    _len = 700
    result=str(data)
    for f in "'{} ":
        result=result.replace(f,"")
    result=result.replace(",",";")
    result=result.replace(":","=")
    result += ";"
    for s in range(_len - len(result)):
        result += "X"
    print(result)
    print(len(result))
    
    message = result
    try:
        reader, writer = await asyncio.open_connection(*ADDRESS)
        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
    except Exception:
        print("ConnectionError")


asyncio.run(tcp_client())