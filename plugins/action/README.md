
# action 
指令系统

## 必须依赖：
```bash
plugins.msg_tools
```

## 导入：

```python
from plugins.action import Action
```

## 使用：
```python=
action = Action(event)
```

## 特性
*pure_msg*   
指的是用户发送的消息本身，但不包括命令前缀，以及任何xml标签。   
如果你的命令前缀不含有空字符串，那么必须要加上命令前缀，否则会直接为空。

## 属性：

```python
self.event: Event  # 事件
self.description: str  # 描述

self.args: list  # 参数
self.text: str  # 文本
```

1.`event`在构造时传入     

2.`description`默认为空，由玩家自定义    

3.`args`在匹配`command`自动填充，为参数列表。   
`cutshort`、`do`情况下为`[]`.   

4.`text`在匹配`cutshort`、`command`、`do`自动填充   
`command`时为参数文本。   
`command`、`do`时为*用户输入*本身。

## 方法：

1.cutshort
```python
action.cutshort(['你好']: list, function: Callable)  # 匹配 cutshort
```
2.command
```python
action.command(['你好']: list, function: Callable)  # 匹配 command
```
3.do
```python
action.do(function: Callable)  # 匹配 do
```
4.send
```python
action.send('你好')  # 发送消息
```


## 混合使用例

```python
@on.message_created
def cck(event: Event):
    action = Action(event)
    action.description = '你是一个一个，一个一个，一个一个，一个大笨蛋'
    action.cutshort(cutshort=['cck'], function=cck_start)  # 匹配 cck
    action.command(command=['cck'], function=cck_end)  # 匹配 cck 开头的命令
    action.cutshort(cutshort=['bzd'], function=cck_end)  # 匹配 bzd

    action.command(command=['cck'], function=cck_guess)  # 匹配 cck 开头的命令
    action.do(function=cck_guess)  # 匹配 任意语句


def cck_start(action: Action):
    action.send('start')


def cck_end(action: Action):
    if '-e' in action.args:
        action.send('我也不知道哦')
    if action.text == 'bzd':
        action.send('我也不知道喵')


def cck_guess(action: Action):
    rpl = action.text
    action.send(f'你猜的是 {rpl}')

```

## 插件

1.help

用于当command参数存在-h时候发送description

2.qq_passive

用于发送qq被动消息

> 在__init__.py中取消导入插件即可取消使用


*end.*



