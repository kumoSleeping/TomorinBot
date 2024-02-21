import os
import sys
import inspect


# 获取当前文件的父目录并切换工作目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
os.chdir(parent_directory)
sys.path.append(parent_directory)


# def chick():
#     import os
#
#     from loader import config
#
#     # 指定modules目录的相对路径
#     modules_path = './modules'
#     init_file_path = os.path.join(modules_path, '__init__.py')
#
#     # 读取__init__.py文件的内容
#     if os.path.exists(init_file_path):
#         with open(init_file_path, 'r') as file:
#             init_content = file.readlines()
#     else:
#         init_content = []
#         # 如果__init__.py不存在，则创建一个空文件
#         with open(init_file_path, 'w') as file:
#             pass
#
#     # 获取modules目录下所有的包（仅顶级）
#     module_dirs = [d for d in os.listdir(modules_path) if os.path.isdir(os.path.join(modules_path, d))]
#     # 删掉一些目录
#     delete_dirs = config['core']['load_ignore_dirs'] if config else ['__pycache__']
#     for d in delete_dirs:
#         if d in module_dirs:
#             module_dirs.remove(d)
#
#     # 检查每个包是否已经在__init__.py中导入或被注释掉
#     for module_dir in module_dirs:
#         # 构造导入语句及其被注释掉的形式
#         import_statement = f'from modules.{module_dir} import *\n'
#         commented_import_statement = f'# from modules.{module_dir} import *\n'
#
#         # 检查是否已经导入或存在注释掉的导入语句
#         if import_statement not in init_content and commented_import_statement not in init_content:
#             init_content.append(commented_import_statement)
#
#     # 更新__init__.py文件
#     with open(init_file_path, 'w') as file:
#         file.writelines(init_content)
#
#     print(f'[load_modules] Updated __init__.py')


def st():
    # chick()
    from core.loader import plugin_manager
    plugin_manager.load_plugins()
    input()


if __name__ == '__main__':
    ascii_tmr = '''

      ██████████╗   ███████╗    
       ╚══██╔████╗ ████╔══██╗   
          ██║██╔████╔██████╔╝   
          ██║██║╚██╔╝██╔══██╗   
          ██║██║ ╚═╝ ██║  █████║   
          ╚═╝╚═╝     ╚═╝  ╚════╝  lite @2023

    '''

    ascii_tmr = '\033[34m' + ascii_tmr + '\033[37m' + '''
    かつて忘れられない、星空は未来を照らし、次の春へ。
    　　　　　　　　　　　　――「未来のある日・東京・豊島区」

     ''' + '\033[0m'

    print(ascii_tmr)
    from loader import config

    if config['core']['hot_reload']:
        import hupper
        reloader = hupper.start_reloader('core.app.st',)

    else:
        st()



