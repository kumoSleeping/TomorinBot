import socket
import zipfile
import os
import threading
from core.loader import config
from core.log import log
from mods.pub import logs

config.need('pub', {'address': '0.0.0.0', 'port': "65432", 'auth_code': '1234ku'})

HOST = config.get_key('pub').get('address')  # Standard loopback interface address (localhost)
PORT = int(config.get_key('pub').get('port'))        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 4096
UPLOAD_FOLDER = './plugs'
AUTH_CODE = config.get_key('pub').get('auth_code')

def receive_file(sock, filename):
    with open(filename, 'wb') as f:
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                break  # 文件接收完毕
            f.write(data)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)  # 删除压缩文件


def verify_client(conn):
    """验证连接的客户端"""
    received_auth = conn.recv(len(AUTH_CODE)).decode()
    return received_auth == AUTH_CODE


def handle_client(conn, addr):
    log.info(f'Connected by {addr}')
    if not verify_client(conn):
        log.error("Authentication failed.")
        conn.close()
        return
    log.success("Authentication successful.")
    zip_path = os.path.join(UPLOAD_FOLDER, f'uploaded_{threading.get_ident()}.zip')
    receive_file(conn, zip_path)
    extract_zip(zip_path, UPLOAD_FOLDER)
    log.error('File uploaded and extracted successfully')
    # 修改触发器文件
    with open('mods/pub/logs.py', 'w') as file:
        # 在文件末尾添加当前时间的注释来触发变化
        file.write(f'# 喵喵喵')
    log.success("Trigger file modified, waiting for hupper to restart the app...")
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        # log.success('Update plugs server listening...')
        log.warning(f'Unsafe: [mods/pub] not recommended for use in production environments.')
        while True:
            conn, addr = s.accept()
            # 对每个客户端连接启动一个新线程
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()



# 线程
t = threading.Thread(target=main, daemon=True)
t.start()


pub_demo =  ''