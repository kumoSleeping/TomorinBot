import argparse
import socket
import zipfile
import os
from io import BytesIO
import json


with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())
    
    
SERVER = config['pub']['address']
PORT = int(config['pub']['port'])


def zip_folder(folder_path, output_stream):
    with zipfile.ZipFile(output_stream, 'w', zipfile.ZIP_DEFLATED) as zipf:
        folder_base = os.path.basename(folder_path)
        for root, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs if d != '__pycache__']  # 过滤掉 __pycache__ 目录
            for file in files:
                if file.endswith('.pyc') or file == '.DS_Store':  # 过滤掉 .pyc 文件和macos下的临时文件
                    continue
                # if file.endswith('.py'):  # 只压缩 .py 文件
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.join(folder_base, os.path.relpath(file_path, folder_path)))

def send_data_with_auth(server_address, port, data, auth_code="AUTH"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_address, port))
        sock.sendall(auth_code.encode())  # 发送验证字节
        sock.sendall(data)  # 然后发送数据
        # print("Data sent successfully")

def main(folder_path):
    output_stream = BytesIO()
    zip_folder(folder_path, output_stream)
    output_stream.seek(0)  # 回到文件的开头
    send_data_with_auth(SERVER, PORT, output_stream.read(), auth_code="1234")
    print("Send completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zip and send a folder over the network")
    parser.add_argument('folder', type=str, help='Path to the folder to zip and send')
    args = parser.parse_args()
    main(args.folder)
