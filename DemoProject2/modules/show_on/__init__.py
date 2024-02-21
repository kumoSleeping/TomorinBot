from typing import Callable, List


def print_on_msg(on_type: str, on_list: List[Callable] = None):
    print(f'\033[31m[core] {on_type}\033[0m')
    if not on_list:
        print('| None |')
        return
    # 找出最长的函数名长度
    max_length = max(len(func.__name__) for func in on_list)
    # 打印表头===
    print('+' + '-' * (max_length + 2) + '+')
    # 打印每个函数名，同时在行尾添加 '|' 并保持对齐
    for func in on_list:
        print('| {:<{}} |'.format(func.__name__, max_length))
    # 打印表尾===
    print('+' + '-' * (max_length + 2) + '+')
    # 清空列表
    del on_list


def return_on_msg(on_type: str, on_list: List[Callable] = None):
    msg = f'\033[31m[core] {on_type}\033[0m\n'
    if not on_list:
        msg += '| None |'
        return msg
    # 找出最长的函数名长度
    max_length = max(len(func.__name__) for func in on_list)
    # 打印表头===
    msg += '+' + '-' * (max_length + 2) + '+\n'
    # 打印每个函数名，同时在行尾添加 '|' 并保持对齐
    for func in on_list:
        msg += '| {:<{}} |\n'.format(func.__name__, max_length)
    # 打印表尾===
    msg += '+' + '-' * (max_length + 2) + '+\n'
    # 清空列表
    del on_list
    return msg


import time
import threading


def start___a():
    from core.loader import plugin_manager
    while True:
        if plugin_manager.is_loaded:
            from core.loader import plugin_manager
            print_on_msg('on类监听', plugin_manager.loaded_func)
            print_on_msg('event生成前勾子函数', plugin_manager.before_event)
            print_on_msg('event生成后勾子函数', plugin_manager.after_event)
            print_on_msg('每个on类监听执行前勾子函数', plugin_manager.before_plugin_do)
            print_on_msg('api请求前勾子函数', plugin_manager.before_request)
            print_on_msg('satori协议请求插件', plugin_manager.satori_post)
            print_on_msg('api请求后勾子函数', plugin_manager.after_request)
            break
        else:
            from core.loader import plugin_manager


t = threading.Thread(target=start___a)
t.start()

from core import on, Event
from modules.command_matcher import match_command


@on.message_created
def show_on_(event: Event):
    from core.loader import plugin_manager
    if res := match_command(event, 'show_on',):
        text = return_on_msg('on类监听', plugin_manager.loaded_func)
        event.message_create(text)





