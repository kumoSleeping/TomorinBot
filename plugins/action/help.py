

def help__(action):
    # -h 为参数的情况
    if action.is_did:
        return action
    if '-h' in action.args:
        action.is_did = True
        output = ''  # 用于存储输出的字符串
        if action.event.platform in ['qq']:
            output += '·\n'  # 在开头加上一个点
        output += '帮助提示：\n'
        # 如果有描述，输出描述
        output += '  ' + action.description + '\n' if action.description != '' else ''
        output = output.strip()  # 去掉最后的换行符

        action.send(output)
        return action
    return action


