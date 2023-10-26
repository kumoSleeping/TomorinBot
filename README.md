


<h1 align="center"> TomorinBOT  </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v0.2.0</div>
<div align="center">  人間になりたいうた...
</div>




<h1 align="center">
  <a href="https://github.com/kumoSleeping/TomorinBot/wiki"> Click Here.> TomorinBOT Wiki</a>
</h1>

***
## イントロダクション




Tomorin项目模版是由Python编写的，代码简约、无异步、轻量的，基于**Satori协议**的的聊天机器人后端**模版框**。   

整体设计灵感来自Koishi，命名灵感来自[MyGO!!!!!](https://zh.moegirl.org.cn/MyGO!!!!!)。

### 実行プロセス 

```mermaid
graph TB
    subgraph ./core
        anonchan.py -- event --> rana.py -- session --> tomorin.py
        tomorin.py -- session --> soyorin.py
        tomorin.py
        soyorin.py -- pass_session --> tomorin.py
        rikki.py
        exit((exit))
    end

    subgraph ./plugins
        index1(plugins_name/index.py > component_2) -- handle --> end_plugin1((end))
        index2(plugins_name/index.py > component_1) -- handle --> send -- handle --> end_plugin2((end))
    end

    tomorin.py -- pass_session --> ./plugins
    soyorin.py -- not_pass_session --> exit
    send -- will_send_session --> rikki.py
    rikki.py -- message_id --> send
    rikki.py -- requests --> http_post[[http_post]]

    subgraph app
    http_post
     websockets[[websockets]] -- event --> anonchan.py 
    end
```

查看[Wiki](https://github.com/kumoSleeping/TomorinBot/wiki/Tomorin-Bot-Core%E6%A6%82%E8%BF%B0)以了解更多。

## フロントエンドサポート


| 前端                  | 可用性 |
|:----------------------|:-------:|
| [koishi-plugin-server]()  | ✅     |
| [go-satori-server]()        | 🫓     |
| [satori.js]()              | 🫓     |
| chronocat             | 🏃     |
| lagrange-satori        | 🏃     |

可以用支持Satori协议的服务连接本项目。

## 機能実現    

以下的链接会跳转到[本项目的Wiki](https://github.com/kumoSleeping/TomorinBot/wiki)。

| 功能                  | 说明 |
|:----------------------|:-------:|
| [ws多例连接](https://github.com/kumoSleeping/TomorinBot/wiki/1.%E4%BD%BF%E7%94%A8)  |      |
| [ws自动重连](https://github.com/kumoSleeping/TomorinBot/wiki/1.%E4%BD%BF%E7%94%A8)  |      |
| [webhook基础连接](https://github.com/kumoSleeping/TomorinBot/wiki/1.%E4%BD%BF%E7%94%A8)   | 利用flask的debug启用dev    |
| [混合连接模式](https://github.com/kumoSleeping/TomorinBot/wiki/1.%E4%BD%BF%E7%94%A8)   | 用于无公网启用dev     |
| [插件包系统](https://github.com/kumoSleeping/TomorinBot/wiki/2.%E5%AE%9E%E7%8E%B0%E5%8A%9F%E8%83%BD)             |      |
| [插件包内组件系统](https://github.com/kumoSleeping/TomorinBot/wiki/2.%E5%AE%9E%E7%8E%B0%E5%8A%9F%E8%83%BD)      |      |
| [help系统]()      |      |
| [黑白名单 组件管理]()      |      |
| [h函数快捷包装元素](https://github.com/kumoSleeping/TomorinBot/wiki/%E6%B6%88%E6%81%AF%E5%85%83%E7%B4%A0)     |     |
| [session抽象](https://github.com/kumoSleeping/TomorinBot/wiki/Session)     |     |
| [bot抽象](https://github.com/kumoSleeping/TomorinBot/wiki/Bot)     |     |
| [send与call_api]()     |     |




## 关于此模版
本模版出发点是学习优秀设计方法，简洁易用。使用此项目的人可以任意修改`./core`中的代码来迎合自己的习惯。   

本项目尽可能的使用简洁美观的方法开发，让简单的功能实现可以高速产出。 


如果你的机器人需要使用较多平台的高级功能，或您习惯使用SDK编写项目，我十分推荐您使用[RF-Tar-Railt/satori-python](https://github.com/RF-Tar-Railt/satori-python/releases/tag/v0.4.0)进行更高级的开发。

## 仓库
由于本人直接在仓库开发BOT   
`.gitignore`规则了忽略了所有`_开头的文件/文件夹`和`config.yml`。

本仓库不存放生产环境插件，但会存放样板插件案例   


------








