import importlib
import inspect
import os
import yaml


config: dict = yaml.safe_load(open('./config.yml', encoding='utf-8'))

loaded_func = {}
satori_post = {}

before_request = {}
before_event = {}
before_plugin_do = {}

after_request = {}
after_event = {}


def load_plugins():
    # 读取config.yml中的插件文件夹
    plugins_dir: list = config['core']['plugins-dir']
    # 按照优先级排序
    plugins_dir.sort(key=lambda x: x['priority'], reverse=True)
    plugins_dir_name = [x['path'] for x in plugins_dir]
    # print(plugins_dir_name)
    # 遍历插件文件夹
    for folder in plugins_dir_name:
        if not os.path.isdir(folder):
            print(f'[load_plugins] \033[31m插件文件夹 [{folder}] 不存在\033[0m continue')
            # 开线程抛出异常
            continue
        print(f'[load_plugins] 正在加载插件包 [{folder}]')

        for plugin_folder in [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]:
            # print(f'[load_plugins] 正在加载插件包 [{plugin_folder}]')
            module = importlib.import_module(f'{folder}.{plugin_folder}')
            for name, obj in inspect.getmembers(module):
                if not (inspect.isfunction(obj) and obj.__module__ == f'{folder}.{plugin_folder}'):
                    continue
                # 这个语句是为了在「不是插件的函数」传递「session」时抛出异常时结束这本次导入 # 故意传递一个空的 session，在对应插件做了异常处理的情况下，这里不会抛出
                if inspect.signature(obj).parameters:
                    try:
                        obj()
                    except:
                        pass
                else:
                    continue
                if hasattr(obj, 'enable_feature'):
                    loaded_func[name] = obj
                    # 绿色字体
                    print(f'\033[32m[load_plugins] [{plugin_folder}] 加载功能 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_before_request'):
                    before_request[name] = obj
                    # 蓝色字体
                    print(f'\033[34m[before_request] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_after_request'):
                    after_request[name] = obj
                    print(f'\033[34m[after_request] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_before_event'):
                    before_event[name] = obj
                    print(f'\033[34m[before_event] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_before_plugin_do'):
                    before_plugin_do[name] = obj
                    print(f'\033[34m[before_plugin_do] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_after_event'):
                    after_event[name] = obj
                    print(f'\033[34m[after_event] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_satori_post'):
                    satori_post[name] = obj
                    print(f'\033[34m[satori_post] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue



