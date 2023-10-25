import re
import json
import base64
import aiohttp
from nonebot import require, on_keyword, on_startswith

require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")

from nonebot_plugin_alconna.uniseg import UniMsg, UniMessage, Image, Reply
from nonebot_plugin_htmlrender import md_to_pic
from nonebot.adapters.red.api.model import ReplyElement
from nonebot.adapters import Bot
from nonebot.drivers import Request


async def request(request: Request):
    async with aiohttp.ClientSession() as session:
        async with session.request(
            request.method, request.url, headers=request.headers, proxy=request.proxy
        ) as response:
            return response.status, await response.text("UTF-8")


def extract_plain_text_from_red_reply_elem(reply_elem: ReplyElement) -> str:
    return "".join([elem["textElemContent"] for elem in reply_elem.sourceMsgTextElems])


def extract_repo_name(url: str):
    parts = url.split("/")
    username = parts[3]
    repo_name = parts[4]
    return f"{username}/{repo_name}"


og = on_keyword(("/",), priority=15, block=False)
readme = on_startswith("/readme", priority=10, block=True)


@og.handle()
async def _(bot: Bot, unimsg: UniMsg):
    message = unimsg.extract_plain_text()

    if message.startswith("https://github.com/"):
        project = extract_repo_name(message)

    else:
        github_repo_pattern = r"^[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+$"
        match = re.match(github_repo_pattern, message)
        if match:
            project = message
        else:
            await og.finish()

    status_code, _ = await request(
        Request("GET", f"https://github.com/{project}", proxy="http://127.0.0.1:7890"),
    )

    if status_code == 200:
        github_url = f"https://github.com/{project}"
        githubcard_url = f"https://opengraph.githubassets.com/githubcard/{project}"

        await og.send(
            github_url + await UniMessage(Image(url=githubcard_url)).export(bot)
        )


@readme.handle()
async def _(bot: Bot, unimsg: UniMsg):
    if Reply not in unimsg:
        await readme.finish()

    reply: ReplyElement = unimsg[Reply][0].origin

    message = extract_plain_text_from_red_reply_elem(reply).replace("[图片]", "")
    if message.startswith("https://github.com/"):
        project = extract_repo_name(message)

    else:
        github_repo_pattern = r"^[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+$"
        match = re.match(github_repo_pattern, message)
        if match:
            project = message
        else:
            await readme.finish()

    status_code, resp = await request(
        Request(
            "GET",
            f"https://api.github.com/repos/{project}/readme",
            proxy="http://127.0.0.1:7890",
            headers={
                "Authorization": "Bearer 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"
            },
        )
    )

    if status_code != 200:
        await readme.finish()

    repo_info = json.loads(resp)

    if not repo_info["content"]:
        await readme.finish()

    repo_readme: str = base64.b64decode(repo_info["content"]).decode("UTF-8")

    await readme.finish(
        await UniMessage(
            Image(
                raw={
                    "data": await md_to_pic(repo_readme, width=1080),
                    "mimetype": "image/png",
                }
            )
        ).export(bot)
    )
