import socket
import json

def listen():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', 45500))
    servidor.listen(1)
    print('[+] Esperando conexión...')
    conn, addr = servidor.accept()
    print(f'[+] Conectado desde {addr}')

    while True:
        comando = input('>>> ')
        if comando == 'salir':
            conn.send(b'salir')
            break
        conn.send(comando.encode())
        respuesta = conn.recv(1024 * 10).decode()
        print(json.loads(respuesta))
    
    conn.close()



if __name__ == '__main__':
    listen()