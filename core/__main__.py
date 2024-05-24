import os
import sys
import inspect
import signal
import importlib
import threading

from core.classes.config import config_pre as config
from core.classes.log import log
from core.classes.log import c
from core.invoker.star import run_on_bot_started_async, run_on_bot_started


# 获取当前文件的父目录并切换工作目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
os.chdir(parent_directory)
sys.path.append(parent_directory)


class IManager:
    def __init__(self):
        self._satori_event = []
        self._startup = []
        self._api_requested = []
        self._event_built = []
        self.loaded = False

    async def load_plugins(self, plugs):
        module_list = [(name, module) for name, module in inspect.getmembers(plugs, inspect.isfunction)]
        for name, module in module_list:
            # 使用字典映射属性到对应的列表
            attr_to_list = {
                '_satori_event': self._satori_event,
                '_startup': self._startup,  # 机器人启动时执行函数
                '_api_requested': self._api_requested,
                '_event_built': self._event_built
            }
            # 检查每个属性并在必要时将函数添加到对应的列表中
            for attr, list_ref in attr_to_list.items():
                # print(attr, list_ref)
                if hasattr(module, attr):
                    if inspect.iscoroutinefunction(module):
                        log.success(f'apply {c.red}async:{c.bright_green}{name} {c.blue}<{getattr(module, attr)}>{c.reset}')
                    else:
                        log.success(f'apply {c.bright_yellow}sync:{c.bright_green}{name} {c.blue}<{getattr(module, attr)}>{c.reset}')
                    list_ref.append(module)
                    break  # 假设一个函数只符合一个分类，找到即停止
        self.loaded = True

    async def auto_load_all_plugins(self):
        # 扫描文件夹下所有表层文件夹
        root_pkg = os.walk('./').__next__()[1]
        root_files = os.walk('./').__next__()[2]
        filtered_folders = [folder for folder in root_pkg if not (folder.startswith(('.', '_', 'core')))]
        filtered_files = [file[:-3] for file in root_files if file.endswith('.py') and not file.startswith(('.', '_'))]
        import_list = filtered_folders + filtered_files
        if len(import_list) == 0:
            log.warning(f'not found {c.red}any{c.reset} {c.bright_magenta}plugs{c.reset}')
        elif len(import_list) == 1:
            log.info(f'found {c.bright_magenta}plug{c.reset}: {c.bright_magenta}{import_list[0]}{c.reset}')
        else:
            log.info(f'found {c.bright_green}{len(import_list)}{c.reset} {c.bright_magenta}plugs{c.reset}: {c.bright_magenta}{' '.join(import_list)}{c.reset}')
        for i in import_list:
            try:
                # 尝试导入模块
                plugs = importlib.import_module(i)
                # 尝试加载插件
                await self.load_plugins(plugs)
            except Exception as e:
                log.error(f'Error occurred while loading {i}: {e}')

    async def run(self):
        await self.auto_load_all_plugins()  # 加载插件
        from core.transmit.ws import start_ws
        await run_on_bot_started_async(self)  # 执行启动函数
        threading.Thread(target=run_on_bot_started, args=(self,)).start()  # 启动函数
        await start_ws()


initialize_manager = IManager()


if __name__ == '__main__':
    import os

    # Windows终端启用ANSI
    if sys.platform == "win32":
        os.system('')  # 这将启用 ANSI 序列支持
    from core.__init__ import __version__
    from core.classes.log import log

    print(
        f'{c.bright_white}B{c.bg.green}OTTo{c.reset}{c.bright_white}morin {c.bright_magenta}v{__version__}{c.reset} {c.white}@2023-2024{c.reset} Compliant with {c.bright_red}Satori Protocol{c.reset}')
    try:
        import asyncio
        asyncio.run(initialize_manager.run())

    except KeyboardInterrupt:
        log.info(f'かつて忘れられない、{c.bg.blue}星空{c.reset}は未来を照らし、次の{c.bg.green}春{c.reset}へ。 ({c.blue}{c.style.underline}2024.1.30 10:54:23・東京・豊島区{c.reset})')
        os.kill(os.getpid(), signal.SIGTERM)











