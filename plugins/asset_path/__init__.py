from core import config
import os
import inspect

if config['asset_path']['assets-dir'] and not os.path.exists(config['asset_path']['assets-dir']):
    os.mkdir(config['asset_path']['assets-dir'])

ASSETS_DIR = config['asset_path']['assets-dir']


def auto_asset_path():
    file_path = inspect.stack()[1].filename
    folder_name = os.path.dirname(file_path)
    pure_folder_name = os.path.basename(folder_name)
    mixed_folder_name = f"{ASSETS_DIR}/{pure_folder_name}"
    # 创建pure_folder_name
    if not os.path.exists(mixed_folder_name):
        os.mkdir(mixed_folder_name)
    return mixed_folder_name



