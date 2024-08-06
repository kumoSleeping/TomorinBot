from tmrn import app
from satori.client import Account
from satori.model import LoginStatus
from tmrn import log, c


@app.lifecycle
async def login_disp(account: Account, event: LoginStatus):
    if event == 2:
        res = await account.login_get()
        name = res.user.name
        if name == '':
            name = 'NO-NAME-BOT'
        status = res.status
        platform = res.platform
        if status == 1:
            log.success(
                f"linked {c.bright_red}Satori Driver{c.reset} {c.bright_yellow}{c.style.bold}{c.style.underline}{name}{c.reset} login {c.bright_green}{platform}{c.reset}.")
        else:
            log.warning(
                f"linked {c.bright_red}Satori Driver{c.reset} {c.bright_yellow}{c.style.bold}{c.style.underline}{name}{c.reset} sleep in {c.bright_green}{platform}{c.reset}.")
    elif event == 1:
        log.info(f"linkin' {c.bright_red}Satori Driver{c.reset}...")

    elif event == 0:
        log.info(f"linkin' {c.bright_red}Satori Driver{c.reset} {c.bright_red}offline{c.reset}.")

