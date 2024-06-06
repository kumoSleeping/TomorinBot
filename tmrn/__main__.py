from os.path import dirname, abspath
from os import chdir
from inspect import currentframe, getfile
from sys import path as sys_path


chdir(dirname(dirname(abspath(getfile(currentframe())))))
sys_path.append(dirname(dirname(abspath(getfile(currentframe())))))


from satori.client import WebsocketsInfo
from tmrn.__init__ import app

import bar  # 导入插件

# app.apply(
#     WebsocketsInfo(
#     ...
#     )
# )


if __name__ == '__main__':
    from inspect import ismodule
    modules = [name for name, module in globals().items() if ismodule(module) and module.__name__ != 'builtins']
    import sys
    import os
    from tmrn import c, log
    # Windows终端启用ANSI
    os.system('') if sys.platform == "win32" else None
    log.info(f'{c.bright_white}t{c.bg.green}m{c.reset}{c.bright_white}rn{c.reset} & {c.bright_red}satori-python{c.reset}: {c.bg.blue}星空{c.reset}は未来を照らし、次の{c.bg.green}春{c.reset}へ。 ({c.blue}{c.style.underline}2024.1.30 10:54:23{c.white} @2023-2024{c.reset}{c.blue}{c.style.underline}・東京・豊島区{c.reset})')
    if modules: [log.success(f'apply {c.bright_yellow}module{c.reset} {c.bright_magenta}{module}{c.reset}') for module in modules]
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level='ERROR')
    from tmrn.__init__ import app
    app.run()
