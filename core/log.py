import yaml
import time

config: dict = yaml.safe_load(open('./config.yml', encoding='utf-8'))


class Log:    
    
    @staticmethod  
    def debug(text):
        '''
        实现自定义print函数 (只有在配置文件启用的时候才会被显示的展示出来)
        Implement custom print function (only displayed when the configuration file is enabled)
        '''
        if config['core']['log']['debug']:
            if config['core']['log']['color']:
                print('\033[1;31m■ ' + text + '\033[0m')
            else:
                print('[DEBUG] ' + str(text))
            
    @staticmethod  
    def error(text):
        if config['core']['log']['color']:
            print('\033[1;31m● ' + text + '\033[0m')
        else:
            print('[ERROR] ' + str(text))
            
    @staticmethod  
    def info(text):
        if config['core']['log']['color']:
            print('\033[1;37m● ' + text + '\033[0m')
        else:
            print('[INFO] ' + str(text))
        
    @staticmethod
    def warning(text):
        if config['core']['log']['color']:
            print('\033[1;33m● ' + text + '\033[0m')
        else:
            print('[WARNING] ' + str(text))
                    
    @staticmethod
    def success(text):
        if config['core']['log']['color']:
            print('\033[1;32m● ' + text + '\033[0m')
        else:
            print('[SUCCESS] ' + str(text))
           
log = Log()


