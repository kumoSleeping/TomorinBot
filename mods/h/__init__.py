import base64
from typing import Union, Optional

import io
from PIL import Image


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

    # @staticmethod
    # def image(param: Union[bytes, str]):
    #     if isinstance(param, bytes):
    #         encoded_image = base64.b64encode(param).decode('utf-8')
    #         return f'<img src="data:image/png;base64,{encoded_image}"/>'
    #     else:
    #         if str(param).startswith("http://") or str(param).startswith("https://"):
    #             return f'<img src="{param}"/>'

    @staticmethod
    def audio(param: Union[bytes, str]):
        if isinstance(param, bytes):
            encoded_audio = base64.b64encode(param).decode('utf-8')
            return f'<audio src="data:audio/mpeg;base64,{encoded_audio}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<audio src="{param}"/>'

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

    @staticmethod
    def image(param: Union[Image.Image, bytes, str]):
        '''
        实现图片的转换
        Implement image conversion

        :param param: Union[Image.Image, bytes, str] PIL图片对象或者图片的二进制数据或者图片的链接
        '''
        if isinstance(param, Image.Image):
            with io.BytesIO() as output:
                param.save(output, format='PNG')
                image_binary = output.getvalue()
            # 将二进制数据转换为Base64编码
            encoded_image = base64.b64encode(image_binary).decode('utf-8')
            # 构建XML格式字符串
            return f'<img src="data:image/png;base64,{encoded_image}"/>'
        elif isinstance(param, bytes):
            encoded_image = base64.b64encode(param).decode('utf-8')
            return f'<img src="data:image/png;base64,{encoded_image}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<img src="{param}"/>'


h = H()

