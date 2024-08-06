import importlib
from tmrn.feat.log import log, c


def load_modules(name: str):
    try:
        importlib.import_module(name)
        log.success(f'import {c.bright_magenta}{name}{c.reset}')
    except ImportError:
        log.error(f'import error:{c.reset} {c.bright_magenta}{name}{c.reset}')
        return False
    except Exception as e:
        log.error(f'import error:{c.reset} {c.bright_magenta}{name}{c.reset} {e}')
        return False

