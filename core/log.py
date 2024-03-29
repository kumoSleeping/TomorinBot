import time
import json
import os


class Log:

    @staticmethod
    def debug(text):
        """
        实现自定义print函数 (只有在配置文件启用的时候才会被显示的展示出来)
        Implement custom print function (only displayed when the configuration file is enabled)
        """
        text = str(text)
        if config["log"]["debug"]:
            if config["log"]["color"]:
                print("\033[1;31m■ " + text + "\033[0m")
            else:
                print("[DEBUG] " + text)

    @staticmethod
    def error(text):
        text = str(text)
        if config["log"]["color"]:
            print("\033[1;31m● " + text + "\033[0m")
        else:
            print("[ERROR] " + text)

    @staticmethod
    def info(text):
        text = str(text)
        if config["log"]["color"]:
            print("\033[1;37m● " + text + "\033[0m")
        else:
            print("[INFO] " + text)

    @staticmethod
    def warning(text):
        text = str(text)
        if config["log"]["color"]:
            print("\033[1;33m● " + text + "\033[0m")
        else:
            print("[WARNING] " + text)

    @staticmethod
    def success(text):
        text = str(text)
        if config["log"]["color"]:
            print("\033[1;32m● " + text + "\033[0m")
        else:
            print("[SUCCESS] " + text)


# log 包是第一个被加载的包，所以在这里初始化配置文件
if not os.path.exists("config.json"):
    with open("config.json", "w", encoding="utf-8") as f:
        f.write(json.dumps({
            "log": {
                "debug": False,
                "color": False
            }
        }, indent=4, ensure_ascii=False))

    with open("config.json", "r", encoding="utf-8") as f:
        config = json.loads(f.read())
    log = Log()
    log.warning("Config file not found, created a new one.")
else:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.loads(f.read())
    log = Log()
