


<h1 align="center"> Tomorin BOT </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v0.2.0</div>
<div align="center">  人間になりたいうた...
</div>


***


## 成员介绍：

Ano.py   
程序启动入口    
对「satori」协议进行连接 / session获取 / 心跳保活   
为每个 session 启动 Main(data)   

Tmorin.py   
Main 处理所有插件   
核心处理调度 data 和 发送

Rana.py   
对「satori」协议进行基础消息抽象 / 日志显示   
提供平台包装元素的 API   

Soyorin.py   
消息审核 / 插件管理 / 黑白名单 API   
与 ./plugin 界限模糊，类似服务组件 API   

Rikki.py   
处理「satori」协议的信息发送 / API上报
```markdown
小知识：
1.程序开始于Ano.py。
2.Rikki.py 只会在 Tmorin.py 被调用。
3.Soyorin.py Tmorin.py 可能永远都不会随着适配器而改变。
4.Tmorin.py 永远是 Bot 的核心。
```


## 快速开始：

```bash
python server.py
# python3 server.py
```

### server.py

启动！

### ./core

首先，被启动的是 `Ano.py` 用于收获来自外界的 **消息** 。

`Ano.py` 收到 **消息** 后，调用 `Tomorin.py` 并传入 **消息** 。

`Tomorin.py` 会调用 `Soyo.py` 的第一部分对 **消息** 解析抽象、审查合格性。

`Soyo.py` 通过后， **消息** 会继续回到 `Tomorin.py` 

`Tomorin.py` 此时获得了 **抽象后的消息** ，此时消息会被 **正式处理** 为 **被发送的消息**。

**正式处理**后，`Tomorin.py` 会调用`Soyo.py` 的第二部分对 **被发送的消息** 进行 打包、审查合格性。

`Soyo.py` 通过后，`Rikki.py` 会被 `Tomorin.py` 作为 **消息发送器** 调用，直接尝试发送 **被发送的消息** 。


### utils.py

修饰器 `@plugin` 将函数视为插件，针对复杂插件可放置于 `./plugin` 下被调用。消息将在 `./plugin` 被处理。



### logger.py

用于记录错误。


### Soyorin.py 特性
当session数据与 忽略体 吻合时