import base64
from typing import Union, Optional


class H:
    @staticmethod
    def text(content: str):
        return f'<content>{content}</content>'

    @staticmethod
    def at(user_id: Union[int, str]):
        return f'<at id="{user_id}"/>'

    @staticmethod
    def sharp(channel_id: Union[int, str]):
        return f'<sharp id="{channel_id}"/>'

    @staticmethod
    def quote(message_id: Union[int, str]):
        return f'<quote id="{message_id}"/>'

    @staticmethod
    def image(param: Union[bytes, str]):
        if isinstance(param, bytes):
            encoded_image = base64.b64encode(param).decode('utf-8')
            return f'<image url="data:image/png;base64,{encoded_image}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<image url="{param}"/>'

    @staticmethod
    def audio(param: Union[bytes, str]):
        if isinstance(param, bytes):
            encoded_audio = base64.b64encode(param).decode('utf-8')
            return f'<audio url="data:audio/mpeg;base64,{encoded_audio}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<audio url="{param}"/>'

    @staticmethod
    def video(param: Union[bytes, str]):
        if isinstance(param, bytes):
            encoded_video = base64.b64encode(param).decode('utf-8')
            return f'<video url="data:video/mp4;base64,{encoded_video}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<video url="{param}"/>'

    @staticmethod
    def file(param: Union[bytes, str]):
        if isinstance(param, bytes):
            encoded_file = base64.b64encode(param).decode('utf-8')
            return f'<file url="data:application/octet-stream;base64,{encoded_file}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<file url="{param}"/>'


import io
from PIL import Image


class HExtension(H):
    @staticmethod
    def qq_passive(param: str):
        return f'<passive passiveId="{param}" />'

    @staticmethod
    def image(param: Union[Image.Image, bytes, str]):
        if isinstance(param, Image.Image):
            with io.BytesIO() as output:
                param.save(output, format='PNG')
                image_binary = output.getvalue()
            # 将二进制数据转换为Base64编码
            encoded_image = base64.b64encode(image_binary).decode('utf-8')
            # 构建XML格式字符串
            return f'<image url="data:image/png;base64,{encoded_image}"/>'
        elif isinstance(param, bytes):
            encoded_image = base64.b64encode(param).decode('utf-8')
            return f'<image url="data:image/png;base64,{encoded_image}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<image url="{param}"/>'


h = HExtension

