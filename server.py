import subprocess
import os


# 获取当前脚本文件所在目录的绝对路径
script_directory = os.path.dirname(os.path.abspath(__file__))
ascii_tmr = '''
     __________________________________
    |                                  |\ 
    |   ████████╗███╗   ███╗██████╗    | |
    |   ╚══██╔══╝████╗ ████║██╔══██╗   | |
    |      ██║   ██╔████╔██║██████╔╝   | |
    |      ██║   ██║╚██╔╝██║██╔══██╗   | |
    |      ██║   ██║ ╚═╝ ██║██║  ██║   | |
    |      ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝   | |
    |                                  | |
    |     欢迎使用 TomorinBOT 项目模版
    |     
    |                                  | |
    |                                  | |
    |                                  | |
    |              春日影                
    |                                  | |
    |                                  | |
    |                                  | |
    |__________________________________| |
     \__________________________________\|   
     
     曾经不会被忘记，星空会照亮未来，下一个春天。
            '''
print(ascii_tmr)

# 我们的迷失，从ano酱开始。（saki？


subprocess.run(["python", script_directory + '/core/ano_sakiyo.py'])

