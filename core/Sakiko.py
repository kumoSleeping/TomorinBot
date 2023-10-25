from flask import Flask, request, jsonify, make_response
import json
import os
import yaml


# 获取当前脚本的目录路径,将当前工作目录切换到脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


script_directory = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录的绝对路径
parent_directory = os.path.dirname(script_directory)  # 获取上一级目录的绝对路径

config = yaml.safe_load(open(str(parent_directory) + '/config.yml', encoding='utf-8'))


from Tomorin import main


app = Flask(__name__)

ascii_ = '''╔════════════════════════╗                           
║       Developing       ║  
╚════════════════════════╝          '''
print(ascii_)

@app.route('/', methods=['POST'])
def webhook():
    data = str(request.json)
    # 在这里处理来自Webhook的数据
    on_message(data)
    response = make_response("OK")

    return response


# 注册 on_message 事件
def on_message(message):
    # print(message)
    data = json.loads(message)
    print(data)
    # data = json.loads(Utils.unescape_special_characters(str(data)))
    main(data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=config["dev"]["port"], debug=True)




