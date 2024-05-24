
# schedule

被装饰的函数被调用了，就单独开设线程，无限跑下去。

## pip
    
```shell
pip install schedule
```

## 使用

```python
from modules import interval_do, timer_do
```
```python
@timer_do(['12:00', '13:00'])
def foo():
    print('foo')

foo()
```

```python
@timer_do('12:00')
def foo():
    print('foo')

foo()
```

```python
@interval_do(60)
def foo():
    print('foo')

foo()
```
    
```python
@interval_do(60, do_now=False)
def foo():
    print('foo')

foo()
```