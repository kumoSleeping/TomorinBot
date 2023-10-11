


<h1 align="center"> Tomorin BOT </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v0.2.0</div>
<div align="center">  人間になりたいうた...
</div>


***

> 快速开始：

```bash
python server.py
# python3 server.py
```

## server.py

启动！

## ./core

首先，被启动的是 `Ano.py` 用于收获来自外界的 **消息** 。

`Ano.py` 收到 **消息** 后，调用 `Tomorin.py` 并传入 **消息** 。

`Tomorin.py` 会调用 `Soyo.py` 的第一部分对 **消息** 解析抽象、审查合格性。

`Soyo.py` 通过后， **消息** 会继续回到 `Tomorin.py` 

`Tomorin.py` 此时获得了 **抽象后的消息** ，此时消息会被 **正式处理** 为 **被发送的消息**。

**正式处理**后，`Tomorin.py` 会调用`Soyo.py` 的第二部分对 **被发送的消息** 进行 打包、审查合格性。

`Soyo.py` 通过后，`Rikki.py` 会被 `Tomorin.py` 作为 **消息发送器** 调用，直接尝试发送 **被发送的消息** 。


## utils.py

修饰器 `@plugin` 将函数视为插件，针对复杂插件可放置于 `./plugin` 下被调用。消息将在 `./plugin` 被处理。



## logger.py

用于记录错误。