from logger import console
import asyncio
import websockets
import json

def show_output(resp):
    output = json.loads(resp)
    console.print(output['stdout'])
    console.print(output['stderr'])

async def shell(websocket):
    while True:
        cmd = console.input('>>> ')
        await websocket.send(cmd)
        if cmd == 'exit':
            break
        resp = await websocket.recv()
        show_output(resp)

async def server(websocket):
    console.log('Cliente conectado')
    resp = await websocket.recv()
    console.log(f'SysInfo: {resp}')
    await shell(websocket)

async def start_server():
    s = await websockets.serve(server, '0.0.0.0', 45500)
    console.log('Esperando conexiones...')
    await asyncio.sleep(30)
    s.close()
    await s.wait_closed()
    console.log('Servidor cerrado')



if __name__ == '__main__':
    asyncio.run(start_server())