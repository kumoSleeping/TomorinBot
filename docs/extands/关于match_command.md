## `match_command` 插件

`match_command` 插件用于匹配用户输入的命令，当用户输入的命令与插件中定义的命令匹配时，插件会执行相应的操作。

```
def match_command(event: Event,
                  command: Optional[Union[List[str], str]] = None,
                  gap_less: bool = False, arg_less: bool = False,
                  admin_only: bool = False,
                  match_args: Optional[Union[List[str], str]] = None,
                  match_text: str = None) -> Optional[MC]:
    '''
    必须参数:
    event 对象  事件对象。
    command  指令头。

    可选参数:
    gap_less  如果为True，指令头不需要空格。
    arg_less  如果为True，指令头后面不能有参数。
    admin_only  如果为True，只有管理员才能触发。（管理员在配置文件里设置）
    match_args  如果有值，只有匹配到了这些参数才会触发。
    match_text  如果有值，只有匹配到了这些文本才会触发，与match_args有一个匹配即可。

    返回:
    Optional[MC] / None  如果匹配到了，返回一个"MC对象"，否则返回None。

    MC对象内含有三个属性：
    event: Event  事件对象本身。
    args: list  指令的参数列表 (不包括指令头)。
    text: str  指令的参数的文本 (去除了指令头的文本)。

    注意：
    必须要命令前缀匹配，才会触发。但如果你的命令前缀有''空字符串，任何消息都会触发。
    命令前缀在配置文件里设置。


    Required parameters:
    event object  Event object.
    command  Command header.

    Optional parameters:
    gap_less  If True, the command header does not need a space.
    arg_less  If True, there can be no parameters after the command header.
    admin_only  If True, only administrators can trigger.(Administrator is set in the configuration file)
    match_args  If there is a value, only if these parameters are matched will it be triggered.
    match_text  If there is a value, only if these texts are matched will it be triggered, either match_args or match_text is matched.

    Return:
    Optional[MC] / None  If matched, return a "MC object", otherwise return None.

    The MC object contains three attributes:
    event: Event  The event object itself.
    args: list  The list of command parameters (excluding the command header).
    text: str  The text of the command parameters (the text of the command header is removed).

    Note:
    Must match the command prefix to trigger. But if your command prefix is an empty string, any message will trigger.
    The command prefix is set in the configuration file.
    '''
```

函数文档给出了足够丰富的提示，这里再补充一些使用方法。


## 匹配任意消息

```py
if res := match_command(event)
```

## 匹配某一个消息 + 任意消息，获取相同 text

```py
if res := match_command(event, ["猜谱面", ""]):
```

上面的代码可以同时匹配 `猜谱面 xxx` 和 `xxx`
同时 `res.text` 都会是 `xxx`

## 匹配参数

```py
if res := match_command(event, ["猜谱面 -e"]):
```

```py
if res := match_command(event, ["猜谱面"], match_args=["-e"]):
```

其实更推荐使用第一种写法，第二种可能在未来的版本中会被废弃。


## 适配QQ (修改模块)

```py
seq = 1


class MC:
    def __init__(self, event: Event, args: list, text: str):
        ...

    def send(self, content: str):
        global seq
        # seq 自增
        seq += 1
        log.debug('seq: ' + str(seq))
        msg = content + f'<passive id="{self.event.message.id}" seq="{seq}"/>'
        return self.event.message_create(content=msg)
```