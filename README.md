


<h1 align="center"> TomorinBOT  </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v0.2.0</div>
<div align="center">  人間になりたいうた...
</div>




<h1 align="center">
  <a href="https://github.com/kumoSleeping/TomorinBot/wiki"> Click Here.> Core WIKI</a>
</h1>

***
## イントロダクション


Tomorin项目模版是由Python编写的，代码简约、轻小、无异步、线程化、插件化，基于**Satori协议**的的聊天机器人后端**模版框**。   

整体设计灵感来自Koishi，命名来自[MyGO!!!!!](https://zh.moegirl.org.cn/MyGO!!!!!)。




## フロントエンドサポート


| 前端                  | 可用性 |
|:----------------------|:-------:|
| [koishi-plugin-server]()  | ✅     |
| [go-qq2str]()              | 🔧     |
| [satori.js]()              | 🫓     |
| chronocat             | ✅🏃     |

可以用支持Satori协议的服务连接本项目。




### 核心

```mermaid

classDiagram
    class core {        
    }

    core : @on.satori_post
    core : @on.before_request
    core : @on.after_request
    core : @before_event
    core : @after_event
    core : @before_plugin_do
    core : @loaded_func[任意标准事件 / 内部接口]
    core : main (function)
    core : Event (class)
    core : config (dict)
    core : on (decorator)
    

    class __init__{
        <<init>>
        向外提供导入
        main (function)
        Event (class)
        config (dict)
        on (decorator)
    }
    class loader{
        记录注册
        loaded_func(dict)
        satori_post(dict)

        before_request(dict)
        before_event(dict)
        before_plugin_do(dict)

        after_request(dict)
        after_event(dict)
    }
    class request{
        发送api请求
        实现三种注册
        on.before_request(decorator)
        on.after_request(decorator)
        on.satori_post(decorator)
        
    }
    class on{
        提供事件装饰器
        注册装饰器
    }
    class main{
        接收data
        实现三种注册
        on.before_event(decorator)
        on.after_event(decorator)
        on.before_plugin_do(decorator)
        on.loaded_func[标准事件](decorator)
        on.loaded_func[内部接口](decorator)
    }
    class app{
        <<启动项目>>
        切换目录
        调用loader
    }
    class event{
        提供satori基础属性
        方法
    }

    __init__ --|> core : 提供接口
    loader --|> core : 记录注册
    request --|> core : 发送请求、注册
    on --|> core : 事件、注册装饰器
    main --|> core : 数据接收、注册
    app --|> core : 启动项目
    event --|> core : 提供基础属性、方法


```





## 关于此模版
本模版出发点是学习优秀设计方法，简洁易用，让简单的功能实现可以高速产出。 


如果您习惯使用SDK编写项目，我十分推荐您使用[RF-Tar-Railt/satori-python](https://github.com/RF-Tar-Railt/satori-python/releases/tag/v0.4.0)进行更开发。

## 仓库
`.gitignore`规则了忽略了所有的`config.yml`。


------



