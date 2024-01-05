import importlib
import inspect
import os
import yaml
import ast


def find_duplicate_function_definitions(source_code):
    """查找重复的函数定义，并给出函数起始行号"""
    with open(source_code, "r") as file:
        tree = ast.parse(file.read(), filename=source_code)

    function_definitions = {}
    for node in ast.walk(tree):
        # 检查是否为顶层函数定义（不在类或函数内）
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            if function_name not in function_definitions:
                function_definitions[function_name] = {"count": 0, "lines": []}
            function_definitions[function_name]["count"] += 1
            function_definitions[function_name]["lines"].append(node.lineno)

    duplicates = {name: info for name, info in function_definitions.items() if info["count"] > 1}
    return duplicates


def find_long_functions(source_code, max_length=50):
    """查找过长的函数，并给出函数起始行号"""
    with open(source_code, "r") as file:
        tree = ast.parse(file.read(), filename=source_code)

    long_functions = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if len(node.body) > max_length:
                long_functions[node.name] = node.lineno

    return long_functions


def find_deep_nesting(source_code, max_depth=3):
    """查找深层嵌套，并给出最深嵌套结构的起始行号"""
    with open(source_code, "r") as file:
        tree = ast.parse(file.read(), filename=source_code)

    deep_nestings = []

    def walk(node, depth, lineno):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
            if depth >= max_depth:
                deep_nestings.append((lineno, depth))
            depth += 1

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                next_lineno = child.lineno
            else:
                next_lineno = lineno
            walk(child, depth, next_lineno)

    walk(tree, 0, 0)
    return deep_nestings


def code_static_check(file_path):
    duplicates = find_duplicate_function_definitions(file_path + '/' + '__init__.py')
    if duplicates:
        print(f'[code_debug] \033[31m [{file_path}] 可能存在重复函数定义: {duplicates} \033[0m')
    long_functions = find_long_functions(file_path + '/' + '__init__.py')
    if long_functions:
        print(f'[code_debug] \033[33m [{file_path}] 可能存在过长的函数: {long_functions} \033[0m')
    deep_nestings = find_deep_nesting(file_path + '/' + '__init__.py')
    if deep_nestings:
        print(f'[code_debug] \033[33m [{file_path}] 可能存在深层嵌套: {deep_nestings} \033[0m')


config: dict = yaml.safe_load(open('./config.yml', encoding='utf-8'))


loaded_func = []
satori_post = []

before_request = []
before_event = []
before_plugin_do = []

after_request = []
after_event = []


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

        # 静态检查
        core_config = config.get('core', {})
        plugins_dir = core_config.get('plugins-dir', [])
        for plugin in plugins_dir:
            if plugin['path'] != folder:
                continue
            static_check = plugin.get('static_check', False)  # 默认值为 False
            break
        else:
            static_check = False

        # 遍历插件文件夹
        for plugin_folder in [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]: # 遍历插件文件夹
            # print(f'[load_plugins] 正在加载插件包 [{plugin_folder}]')

            module = importlib.import_module(f'{folder}.{plugin_folder}') # 导入插件包
            # 代码静态检查
            if static_check:
                code_static_check(f'{folder}/{plugin_folder}')

            # 遍历插件包中的函数
            for name, obj in inspect.getmembers(module):
                if not (inspect.isfunction(obj) and obj.__module__ == f'{folder}.{plugin_folder}'):
                    continue

                # 过滤掉非内部函数
                if not inspect.signature(obj).parameters:
                    continue

                # 属性标记在装饰器中已经完成
                if hasattr(obj, 'enable_feature'):
                    loaded_func.append(obj)                    # 绿色字体
                    print(f'\033[32m[load_plugins] [{plugin_folder}] 加载功能 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_before_request'):
                    before_request.append(obj)
                    # 蓝色字体
                    print(f'\033[34m[before_request] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_after_request'):
                    after_request.append(obj)
                    print(f'\033[34m[after_request] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_before_event'):
                    before_event.append(obj)
                    print(f'\033[34m[before_event] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_before_plugin_do'):
                    before_plugin_do.append(obj)
                    print(f'\033[34m[before_plugin_do] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_after_event'):
                    after_event.append(obj)
                    print(f'\033[34m[after_event] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue
                if hasattr(obj, 'is_satori_post'):
                    satori_post.append(obj)
                    print(f'\033[34m[satori_post] [{plugin_folder}] 注册 [{obj.__name__}]\033[0m')
                    continue



