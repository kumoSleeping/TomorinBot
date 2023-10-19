import os
import importlib
import sys
from plugin_package.component import component_configurations

from core.Rana import Rana
from core.Soyorin import BanManager
# from core.Soyorin import Utils

'''
Tmorin.py
处理所有插件
核心处理调度 data 和 发送
'''

sys.path.append("..")  # 添加上一级目录到模块搜索路径

# 获取目标包下的所有文件夹
subdirectories = [d for d in os.listdir('plugin_package')
                  if os.path.isdir(os.path.join('plugin_package', d)) and not d.startswith('_')]
formatted_subdirectories = ['插件包[' + folder + ']加载成功！' for folder in subdirectories]

notice = '\n'.join(formatted_subdirectories)
print(notice)


def main(data):
    session = Rana.process_satori_message(data)
    # 插件管理 / 黑名单审查

    for plugin in component_configurations:
        if not BanManager.check_before_plugin(session, str(plugin).split()[1]):
            # print('[WARNING] 消息被soyorin拦截...')
            continue
        plugin(session)

    for folder in subdirectories:
        try:
            # 使用importlib动态导入模块
            module = importlib.import_module(f'plugin_package.{folder}.index')
            if not BanManager.check_before_plugin(session, folder):
                # print('[WARNING] 消息被soyorin拦截...')
                continue

            # 调用模块中的src函数
            module.src(session)
        except ImportError as e:
            print(f"Failed to import module {folder}: {str(e)}")
        except AttributeError:
            print(f"Module {folder} does not have a src() function.")


print('Tomorin.py 导入插件结束\n当前 Tomorin 框架版本：[ 人間になりたいうた ]')




