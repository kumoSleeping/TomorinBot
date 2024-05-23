import inspect

from core.classes.log import log
from core.classes.log import c


async def run_on_bot_started_async(initialize_manager):
    if len(initialize_manager._startup) > 0:
        for func in initialize_manager._startup:
            if inspect.iscoroutinefunction(func):
                try:
                    await func()
                    log.info(f"executed {c.bright_green}{func.__name__}{c.reset} {c.blue}<bot_started>{c.reset}")
                except Exception as e:
                    log.error(f"Error in {c.blue}<bot_started>{c.reset} function {func.__name__}: {e}")
    else:
        # log.info(f'not found any {c.blue}<bot_started>{c.reset}')
        pass


def run_on_bot_started(initialize_manager):
    if len(initialize_manager._startup) > 0:
        for func in initialize_manager._startup:
            if not inspect.iscoroutinefunction(func):
                try:
                    func()
                    log.info(f"executed {c.bright_green}{func.__name__}{c.reset} {c.blue}<bot_started>{c.reset}")
                except Exception as e:
                    log.error(f"Error in {c.blue}<bot_started>{c.reset} function {func.__name__}: {e}")
    else:
        # log.info(f'not found any {c.blue}<bot_started>{c.reset}')
        pass





