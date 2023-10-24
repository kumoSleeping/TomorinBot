


<h1 align="center"> Tomorin BOT  </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v0.2.0</div>
<div align="center">  人間になりたいうた...
</div>




<h1 align="center">
  <a href="https://github.com/你的用户名/你的项目名称/wiki">Tomorin BOT Wiki</a>
</h1>

***
## 概述

### 介绍

Tomorin项目模版是由Python编写的，代码简约、无异步、轻量的，基于**Satori协议**的的聊天机器人后端**模版项目**。   

整体设计灵感来自Koishi，命名灵感来自MyGO!!!!!


### 前端支持


| 前端                  | 可用性 |
|:----------------------|:-------:|
| koishi-plugin-server  | ✅     |
| go-satori-server        | 🫓     |
| satori.js              | 🫓     |
| chronocat             | 🏃     |
| lagrange-satori        | 🏃     |

可以用支持Satori协议的服务连接本项目。

### 模版实现    
1.ws连接到satori协议前端，根据yml文件支持多例。    
2.h包装富元素，session、bot属性抽象。    
3.dev下利用flask热重载(此dev可连接webhook)。    
4.插件包系统内部支持多组件，支持help <组件名> 。     
5.提供一套名为ign的黑白名单，插件/组件管理。   

### 关于此模版
本模版出发点是学习优秀设计方法，简洁易用。使用此项目的人可以任意修改`./core`中的代码来迎合自己的习惯。   

本项目尽可能的使用简洁美观的方法开发，让简单的功能实现可以高速产出。 


如果你的机器人需要利用代码平台的高级功能较多，或您习惯SDK编写项目，我十分推荐您使用[RF-Tar-Railt/satori-python](https://github.com/RF-Tar-Railt/satori-python/releases/tag/v0.4.0)进行更高级的开发。

------


[项目的Wiki](https://github.com/kumoSleeping/TomorinBOT/wiki)






