from enum import IntEnum
from typing import Union, Optional
import re

from core.config import config
from core.session_maker import Session, Message
from core.api import Api


class Arg:
    def __init__(self, name: str = None, description: str = ''):
        self.name: str = name
        self.description: str = description


class Examples:
    def __init__(self, examples=None):
        if examples is None:
            examples = []
        self.list_all: list = examples

    def add(self, name: str = None, description: str = ''):  # 添加参数
        arg = Arg(name, description)
        self.list_all.append(arg)
        return self

    def output(self) -> list:
        return self.list_all


class Function:
    def __init__(self, names: list = None, description: str = ''):
        self.description: str = description
        self.names_list: list = names
        self.examples: Optional[Examples] = Examples()


class Command:
    def __init__(self, name: str = None, args: list = None, text: str = ''):
        self.name: str = name
        self.args: list = args
        self.text: str = text


class MessageExtension(Message):
    def __init__(self, message_info: dict):
        super().__init__(message_info)
        self.command: Optional[Command] = Command()


class SessionExtension(Session):
    def __init__(self, body: dict):
        super().__init__(body)
        self.function: Optional[Function] = Function()
        self.message: Optional[MessageExtension] = MessageExtension(self.data.get('message', {}))

        if '' == self.message.content and self.type == 'message-created':
            msg = "".join(element['attrs']['content'] for element in self.data['message']['elements'] if element['type'] == 'text')
            self.message.content = msg.strip()  # 空格不需要了
        self.seq = 0  # 将 seq 定义为实例属性

    def send(self, message_content: str):
        # 使用实例属性时，直接通过 self 访问

        if self.platform in ['qq', 'qqguild'] and '<passive id=' not in message_content:
            self.seq += 1  # 增加实例属性 seq 的值
            # print(f'[qq-shiter] 当前seq: {self.seq}')
            message_content = message_content + f'<passive id="{self.message.id}" seq="{self.seq}"/>'
            print(f'[ (qq-shiter) < 被动消息 > send -> {self.platform}: {self.channel.id} ] ')
        else:
            print(f'[ send -> {self.platform}: {self.channel.id} ] ')
        return Api.message_create(self, channel_id=self.channel.id or self.guild.id, content=message_content)

    def action(self, actions: dict):

        # None 为参数的情况
        if None in actions and self.message.command.args is None:
            actions[None](self)
            return
        # 对应参数的情况
        if self.message.command.args:
            for arg, func in actions.items():
                # 如果arg是元组，则检查元组中的任一元素是否在self.message.command.args中
                if isinstance(arg, tuple):
                    if any(item in self.message.command.args for item in arg):
                        # 如果匹配，则执行对应的函数
                        func(self)
                        return
                # 如果arg是字符串，则直接检查是否匹配
                elif isinstance(arg, str):
                    if arg in self.message.command.args:
                        func(self)
                        return
        # -h 为参数的情况
        if '-h' in self.message.command.args or '帮助' in self.message.command.args:
            output = ''  # 用于存储输出的字符串
            if self.platform in ['qq', 'qqguild']:
                output += '·\n'  # 在开头加上一个点

            output += f'指令：{self.function.names_list[0]}\n'  # 输出指令名

            # 如果有描述，输出描述
            output += '  ' + self.function.description + '\n' if self.function.description != '' else ''

            other_name = ', '.join(self.function.names_list[1:])
            if other_name != '':
                other_name = f'别名：{other_name}'  # 如果有别名，输出别名
            output += other_name + '\n' if other_name != '' else ''

            all_list = self.function.examples.output()  # 获取所有参数
            if all_list:  # 如果有参数，输出 “指令示例：”
                output += '指令示例：\n'

            for arg in all_list:  # 遍历所有参数
                if arg.name:
                    output += f'  {self.function.names_list[0]} {arg.name} => {arg.description}\n'
                else:
                    output += f'  {self.function.names_list[0]} => {arg.description}\n'

            output = output.strip()  # 去掉最后的换行符

            self.send(output)
            return
        # True 为参数的情况
        if True in actions:
            actions[True](self)
            return


#         if '-h' in self.message.command.args or '帮助' in self.message.command.args:
#             def add_indentation(text):
#                 # 分割文本到单独的行
#                 lines = text.split('\n')
#                 # 给每行添加四个空格
#                 indented_lines = ['    ' + line for line in lines]
#                 # 将修改后的行合并回一个字符串
#                 indented_text = '\n'.join(indented_lines)
#                 return indented_text
#             cmd_name = config["bot"]["prefix"][0] + self.function.command_list[0]
#             other_name = ', '.join(self.function.command_list[1:])
#             if other_name != '':
#                 other_name = f'\n别名：{other_name}'
#             doc_ = ''
#             main_doc = add_indentation(self.function.doc.replace('    ', '').strip())
#             for k, v in actions.items():
#                 # 如果k不是字符串
#                 # if not isinstance(k, str):
#                 #     continue
#                 if v:
#                     if not v.__doc__:
#                         continue
#                     if not k:
#                         action_doc = v.__doc__.strip().replace('\n', '，').replace(' ', '')
#                         doc_ += f'    {cmd_name}    {action_doc}\n'
#                         continue
#                     action_doc = v.__doc__.strip().replace('\n', '，').replace(' ', '')
#                     doc_ += f'    {cmd_name} {k}    {action_doc}\n'
#             if doc_.endswith('\n'):
#                 doc_ = doc_[:-1]
#             eg_ = ''
#             if self.function.arg_examples:
#                 for example in self.function.arg_examples:
#                     eg_ += f'\n    {cmd_name} {example}'
#             qq = ''
#             if self.platform in ['qq', 'qqguild']:
#                 qq = '·\n'
#             say = '指令示例：\n' if doc_ != '' or eg_ != '' else ''
#             if doc_ == '' and eg_.startswith('\n'):
#                 eg_ = eg_.replace('\n', '', 1)
#             help_doc_processed = f'''{qq}指令: {cmd_name}
# {main_doc}{other_name}
# {say}{doc_}{eg_}
# '''
#             # print('doc_', doc_)
#             # print('eg_', eg_)
#             self.send(help_doc_processed)
#             return