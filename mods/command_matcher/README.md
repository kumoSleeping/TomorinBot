
# command_matcher 
command_matcher指令系统

## 必须依赖：
```bash
plugins.msg_tools
```

## 导入：

```python
from modules import match_command
```

## 使用：
```python
# 最简使用
asc_back = match_command(event, '你好')  # 存在at会检查at me

# 也可以使用列表
asc_back = match_command(event, ['你好', 'hello', 'hi'])

# 强制要求前缀匹配，除非前缀带有 '' 空字符串
# 即使为 false 也会自动处理掉前缀，只是不会强制必须要有
asc_back = asmatch_commandc(event, '你好', force_prefix=True)

# 支持startswith
asc_back = match_command(event, '你好', startswith=True)
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




*end.*



