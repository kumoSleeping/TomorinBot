import time
import requests
import re

from core.Rana import h


def gh_og(session):
    '''
    gh项目生成og图
    监测到 name/reop 或gh仓库链接后 生成 og 图并发送
    '''
    if "/" in session.message.content:
        _fetch_github_data(session)


def _extract_repo_name(url):
    parts = url.split('/')
    username = parts[3]
    repo_name = parts[4]
    return f"{username}/{repo_name}"


def _fetch_github_data(session):
    message = session.message.content
    try:
        if message.startswith('https://github.com/'):
            project = _extract_repo_name(message)
        elif '/' in message:
            github_repo_pattern = r'^[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+$'
            match = re.match(github_repo_pattern, session.message.content)
            if match:
                project = message
            else:
                return
        else:
            print('Invalid input')
            return

        response = requests.get(f'https://github.com/{project}')
        print('请求gh')
        if response.status_code == 200:
            print(f'项目存在: {response.url}')
            github_url = f'https://github.com/{project}'
            githubcard = f'https://opengraph.githubassets.com/githubcard/{project}'
            # if config.show_url:
            #     print(f'{github_url}<image url="{githubcard}"/>')
            # else:
            #    print(f'<image url="{githubcard}"/>')
            session.send(f"{github_url}{h.image(githubcard)}")

        elif response.status_code == 404:
            print('项目不存在')
        else:
            print(f'发生错误: {response.status_code}')
    except Exception as e:
        print(f'发生错误: {e}')




