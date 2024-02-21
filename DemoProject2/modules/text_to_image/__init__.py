from PIL import Image, ImageDraw, ImageFont
from math import ceil
from typing import List, Tuple
import os
import re

# import inspect
# import io
# from memory_profiler import profile
from modules import auto_asset_path
from core.loader import config

current_directory = os.getcwd()
font_path = auto_asset_path() + '/' + config['text_to_image']['font_name']


# @profile
def __words2lines(words: List[str], width: int, padding: int, fill: Tuple[int, int, int], font: ImageFont.ImageFont, line_spacing: int) -> List[dict]:
    # 可以换行的标点符号
    symbols = ['，', '。', '！', '？', '；', '：', '…', '—', '.', ',', '?', '!', ';', ':', '-', '、', 'ー', "’", "”"]

    # 获取单个词语的宽度
    def get_word_width(word: str) -> int:
        return ceil(font.getlength(word))

    # 获取单行文字的高度
    line_height = ceil(font.getbbox("戸山香澄ToyamaKasumi")[3])

    # 初始化变量
    x, y = padding, padding
    is_wraped = False  # 是否需要换行
    lines = []  # 存储行信息的列表

    # 逐个词语进行处理
    for index, word in enumerate(words):
        # 如果当前行可以放下这个词语
        if x + get_word_width(word) <= width - padding:
            # 处理换行符
            y += (line_height + 2 * line_spacing) * word.count("\n")
            x += get_word_width(lines[index - 1]["text"]) if is_wraped else 0
            y += line_spacing if is_wraped else 0
            # 记录该词语的信息
            lines.append({
                "xy": (x, y),
                "text": word.replace("\n", ""),
                "fill": fill,
                "font": font
            })
            x = x + get_word_width(word.replace("\n", "")) if word.count("\n") == 0 else padding
            is_wraped = False
        # 如果当前行放不下这个词语
        else:
            # 处理换行符
            y += (line_height + 2 * line_spacing) * (word.count("\n") + 1)
            x = padding
            is_wraped = True
            # 记录该词语的信息
            if word not in symbols:
                lines.append({
                    "xy": (x, y + line_spacing),
                    "text": word.replace("\n", ""),
                    "fill": fill,
                    "font": font
                })
            else:
                lines[index - 1]["xy"] = (x, y)
                x += get_word_width(lines[index - 1]["text"])
                lines.append({
                    "xy": (x, y),
                    "text": word.replace("\n", ""),
                    "fill": fill,
                    "font": font
                })
    return lines


# @profile
def text2img(text: str,
                fill: tuple = (0, 0, 0),
                bg_fill: tuple = (255, 254, 236),
                line_spacing: int = 6) -> Image.Image:
    '''
    必须参数:
    text: 文本

    可选参数:
    fill: 文本颜色
    bg_fill: 背景颜色
    line_spacing: 行间距

    返回值:
    Image.Image: 图片对象


    Required parameters:
    text: text

    Optional parameters:
    fill: text color
    bg_fill: background color
    line_spacing: line spacing

    Return value:
    Image.Image: image object
    '''
    # 更新正则表达式以包括包含空格的英语单词或短语
    # \u4e00-\u9fff: 中文字符
    # \u3040-\u309F: 平假名
    # \u30A0-\u30FF: 片假名
    # [a-zA-Z]+(?:\s[a-zA-Z]+)*: 英语单词或短语，可能包含空格
    # \d+: 数字
    # .: 其他所有字符
    # pattern = r'[\u4e00-\u9fff\u3040-\u309F\u30A0-\u30FF]+|[a-zA-Z]+(?:\s[a-zA-Z]+)*|\d+|.'
    # words = re.findall(pattern, text)
    # 匹配所有字符
    words = re.findall(r'[a-zA-Z]+|\d+|\s|.', text)
    font: ImageFont.ImageFont = ImageFont.truetype(font=os.path.join(current_directory, font_path), size=36)

    width = int(len(words)*2 + 600)
    padding: int = int(width // 20)

    data = __words2lines(words, width, padding, fill, font, line_spacing)
    height = max(i["xy"][1] for i in data) + padding + ceil(font.getbbox("戸山香澄ToyamaKasumi")[3])
    result = Image.new("RGBA", (width, height), bg_fill)
    draw = ImageDraw.Draw(result)
    # 行数
    for item in data:
        if item["text"] != '':
            draw.text(item["xy"], item["text"], item["fill"], item["font"])

    return result


# @profile
# def test():
#     # 示例文本
#     text = '''
# 我知道，我不会再回到这里了，无论是，是…
# 顷刻间，倾盆大雨浇透了祥子，膝盖上淡淡的血迹混着雨滴，半边折断的透明伞面也被路边的石头磨破…从未出现过冰冷从一切地方汇入她。雨水混杂泪水，视线早已模糊。血滴被暴雨冲洗，滴落在泥路上已褪色的花瓣上。
# 恍惚间，她似乎心头一震。汽车从桥下呼啸而过，冷，冷，雨水掺着泥泞在地上爬行，将滴落下的一切都送进下水道。
# “一切都是…有生命的…这些残花，都是生命凋零过的痕迹吧。”
# 如果就在这里结束…
#
# 空气冷的要命，潮湿的空气夹着甜腥味，视线又模糊了起来…她感觉到自己的在下沉。
# 无论多少次，她都害怕再一次见到到那个雨天。
# 恍惚间，一路街灯似彩。
# 华灯与商场的音乐侵蚀了本不存在氛围，初春的空气渲染着一种难以言说的气氛。仿佛每个春天的故事，都被这份气息所包容，无论结束与开始。
# 她想起来了，她又逃走了。
# 如果是为了背负所谓命运，就一路的逃避…
# 真想忘掉…我已经，不能再忘记了…
#
# “那就，由我来亲手书写，下一个春天的故事。”
#  '''
#
#     # 示例配置
#     pil = text2img(text)
#
#     pil.show()  # 关闭BytesIO对象
#
#
# if __name__ == '__main__':
#     test()