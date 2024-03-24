# pub


用于在不同tomorin实例之间传递插件


config:

```yml
pub:
  address: '127.0.0.1'
  port: 65432
  auth_code: '123456'
```


```bash
python mods/pub ./plugs/echo
# python3 mods/pub ./plugs/echo
```


会将plugs/echo插件发布到 `address:port` 指定的 `tomorin` 实例上的 `plus` 文件夹中。



