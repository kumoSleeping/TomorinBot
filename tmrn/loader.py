import importlib
from tmrn.log import log, c


def load_modules(name: str):

    importlib.import_module(name)
    log.success(f'import {c.bright_magenta}{name}{c.reset}')

