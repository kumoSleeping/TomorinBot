
from bridge.session_adder import SessionExtension
from session_utils import show_session_log, show_session_data
from load_plugins import plugin_loader

'''
处理所有插件
核心处理调度 data 和 发送
'''

function_info_list = []


def main(data):
    # 展示data
    # show_session_data(data)
    session = SessionExtension(data)
    # 控制台输出
    try:
        show_session_log(session)
        pass
    except Exception as e:
        print(f'[Error] Rana 抛出 {e}')

    for plugin_name in plugin_loader.loaded_plugins:
        plugin_loader.execute_plugin(session, plugin_name)





