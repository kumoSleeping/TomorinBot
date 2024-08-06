from satori.client import WebsocketsInfo
from tmrn.start import app, run
from tmrn import load_modules


# app.apply(
#     WebsocketsInfo(
#     ...
#     )
# )

load_modules('tmrn.disp.login_disp')
load_modules('tmrn.disp.msg_disp')
load_modules('bar')
load_modules('foo')
# load_modules('tsugu_bot')

run()
