import subprocess
import os


# 获取当前脚本文件所在目录的绝对路径
script_directory = os.path.dirname(os.path.abspath(__file__))
ascii_tmr = '''

  ██████████╗   ███████╗    
   ╚══██╔████╗ ████╔══██╗   
      ██║██╔████╔██████╔╝   
      ██║██║╚██╔╝██╔══██╗   
      ██║██║ ╚═╝ ██║  █████║   
      ╚═╝╚═╝     ╚═╝  ╚════╝  lite @2023

'''

ascii_tmr = '\033[34m' + ascii_tmr + '\033[37m' + '''
曾经不会被忘记，星空会照亮未来，下一个春天。
               ———— 《未来的某一天·Tokyo·豊島区》
 
 ''' + '\033[0m'

print(ascii_tmr)

# 我们的迷失，从ano酱开始。（saki？


try:
    subprocess.run(["python", script_directory + '/core/app.py'])
except:
    try:
        print('[Python] 检测到您的系统路径没有Python，正在尝试使用Python3运行')
        subprocess.run(["python3", script_directory + '/core/app.py'])
    except:
        exit(1)
