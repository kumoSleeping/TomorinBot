from satori.client import Account, App
from tmrn.feat.log import log, c
from sys import platform, stdout
from os.path import dirname, abspath
from os import chdir, system
from inspect import currentframe, getfile
from sys import path as sys_path
from tmrn.feat.end import end_
import bestdori


chdir(dirname(dirname(abspath(getfile(currentframe())))))
sys_path.append(dirname(dirname(abspath(getfile(currentframe())))))


# Windows终端启用ANSI
system('') if platform == "win32" else None
log.info(f'{c.bright_white}t{c.bg.green}m{c.reset}{c.bright_white}rn{c.reset} & {c.bright_red}s-p{c.reset}')


app = App()


def run():
    from loguru import logger
    logger.remove()
    # 关闭satori-python的日志输出
    logger.add(stdout, level='ERROR')
    from tmrn import app
    app.run()
    end_()

