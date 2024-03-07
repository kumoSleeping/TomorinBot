# from typing import Callable, List
# import threading
#
#
# def format_msg(on_list: List[Callable] = None):
#     msg = '\n'
#     if not on_list:
#         msg += '| None |'
#         return msg
#     # 找出最长的函数名长度
#     max_length = max(len(func.__name__) for func in on_list)
#     # 打印表头===
#     msg += '+' + '-' * (max_length + 2) + '+\n'
#     # 打印每个函数名，同时在行尾添加 '|' 并保持对齐
#     for func in on_list:
#         msg += '| {:<{}} |\n'.format(func.__name__, max_length)
#     # 打印表尾===
#     msg += '+' + '-' * (max_length + 2) + '+\n'
#     # 清空列表
#     del on_list
#     return msg
#
#
# def start___a():
#     from core.loader import plugin_manager
#     while True:
#         if plugin_manager.is_loaded:
#             from core.loader import plugin_manager
#             # 混合所以on类监听函数
#             all_on = plugin_manager.loaded_func + plugin_manager.satori_post + plugin_manager.before_request + plugin_manager.before_event + plugin_manager.before_plugin_do + plugin_manager.after_request + plugin_manager.after_event
#             formatted_msg = format_msg( all_on)
#             print(formatted_msg)
#             break
#         else:
#             from core.loader import plugin_manager
#
#
# t = threading.Thread(target=start___a)
# t.start()
#
#
