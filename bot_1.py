from satori.client import WebsocketsInfo
from tmrn.start import app, run
from tmrn import load_modules


app.apply(WebsocketsInfo(                                                                                                                                                                                                                                                           host='124.221.153.148', port=5501,token="f7e840aa7f4da1cb71ba943a8bbb3de0fc914e3a10e3b50322b3093bb24ab695"))


load_modules('tmrn.disp.login_disp')
load_modules('tmrn.disp.msg_disp')
# load_modules('kmk')
load_modules('test')
# load_modules('foo')
# load_modules('tsugu_bot.tsugu')


run()
