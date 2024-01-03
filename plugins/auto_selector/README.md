
# auto_selector 
auto_selector指令系统

## 必须依赖：
```bash
plugins.msg_tools
```

## 导入：

```python
from plugins.auto_selector import asc
```

## 使用：
```python
asc_back = asc(event, command=['你好'], perfix=False)
```

## 返回

当`message`匹配到`command`时，返回`ACS类的实例`

```python
self.args: list  # 参数
self.text: str  # 文本
```
否则返回`False`

## 方法：

1.send（可用于兼容qq适配器，暂未实现）


## 使用例（状态码猫图）：

asc通常与海象表达式一起使用，以便在一行内完成两种判断。


```python
from plugins.auto_selector import asc

@on.message_created
def cat_code(event: Event):
    if aps := asc(event, ['状态码猫图', 'scc', 'statuscodecat'], prefix=False):
        try:
            aps.send(h.image("https://httpcats.com/" + aps.args[0] + '.jpg') if aps.args[0].isdigit() else '状态码猫图只能是数字喵')
        except:
            aps.send(f'你家状态码会返回 {aps.args[0]} 喵？')
```


*end.*



