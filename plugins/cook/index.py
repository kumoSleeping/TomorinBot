import re
import json
import random

from bridge.tomorin import h, on_activator, on_event
from plugins.__img_utils.utils import ImageUtils  # 用于生成图片


@on_activator.command(['吃什么', '饿了'])
def eat_what(session):
    """
    吃什么
    随机输出菜谱
    """
    # session.message_create(content=session.command.text)
    if not session.command.args:
        session.send(random_food(select_by_stuff([]), 3))


# 下面都是旧版没有指令系统写的

@on_event.message_created
def food(session):
    """
    查菜谱
    查菜谱 食材1 食材2 ·输出所有菜谱
    查菜谱 菜名 ·查菜谱
    查素菜 食材1 食材2 ·输出所有素菜谱
    查纯素菜 食材1 食材2 ·无豆腐 鸡蛋
    """
    pure_msg = (session.message.content).strip()
    if pure_msg.startswith("查素菜"):
        test_rpl = select_by_name(pure_msg[len("查素菜"):].strip())
        if test_rpl != '':
            session.send(test_rpl)
            return
        tool_list: list = pure_msg[len("查素菜"):].strip().split()
        all_food = _all_food(select_by_stuff(tool_list))
        session.send(all_food)
    if pure_msg.startswith("查素菜"):
        tool_list: list = pure_msg[len("查素菜"):].strip().split()
        all_food = _all_food(select_by_stuff(tool_list, 'all'))
        session.send(all_food)
    if pure_msg.startswith("查纯素菜"):
        tool_list: list = pure_msg[len("查纯素菜"):].strip().split()
        all_food = _all_food(select_by_stuff(tool_list,'pure'))
        session.send(all_food)


def download():
    import requests

    url = "https://cook.yunyoujun.cn/_nuxt/recipe.bc08e6a8.js"

    # 发送GET请求并获取响应
    response = requests.get(url)

    # 检查响应状态码，200表示成功
    if response.status_code == 200:
        # 获取响应内容并以UTF-8编码解码
        data = response.content.decode('utf-8')
        # print(data)

        # 使用正则表达式清理数据
        data_cleaned = re.sub(r'\s+', '', data)  # 删除所有空格和换行符
        data = re.sub(r'(\w+):', r'"\1":', data_cleaned)  # 替换属性名的单引号为双引号

        # 从JavaScript代码中提取数据部分
        start = data.find("[{")
        end = data.rfind("}]") + 2
        json_data = data[start:end]
        print(json_data)

        # 将提取的数据部分转换为JSON
        parsed_data = json.loads(json_data)
        with open('data.json', 'w', encoding='utf-8') as json_file:
            json.dump(parsed_data, json_file, ensure_ascii=False, indent=2)

        # 打印JSON数据
    else:
        print("请求失败，状态码:", response.status_code)


# _download()


# 处理emoji，将emoji转化为中文并删除重复
def process_emoji(emoji_list):
    emoji_dict = {
        "🥔": "土豆", "🥕": "胡萝卜", "🥦": "花菜", "🥣": "白萝卜",
        "🥒": "西葫芦", "🍅": "番茄", "🥬": "芹菜", "🥒": "黄瓜",
        "🧅": "洋葱", "🎍": "莴笋", "🍄": "菌菇", "🍆": "茄子",
        "🍲": "豆腐", "🥗": "包菜", "🥬": "白菜",
        "🍝": "面食", "🍞": "面包", "🍚": "米", "🍜": "方便面",
        "🥓": "午餐肉", "🌭": "香肠", "🌭": "腊肠", "🐤": "鸡肉",
        "🐷": "猪肉", "🥚": "鸡蛋", "🦐": "虾", "🐮": "牛肉", "🦴": "骨头"
    }
    emoji_list = [emoji_dict.get(emoji, emoji) for emoji in emoji_list]
    emoji_list = list(set(emoji_list))  # 删除重复元素
    return emoji_list


# 匹配stuff中包含列表元素的项并返回
def select_by_stuff(target_list, material=None):
    matching_items = []
    with open('./plugins/_cook/data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    if material:
        if material == 'pure':
            vegetable_tools = ["土豆", "胡萝卜", "花菜", "白萝卜", "西葫芦", "番茄", "芹菜", "黄瓜", "洋葱", "莴笋", "菌菇", "茄子", "包菜", "白菜"]
        elif material == 'all':
            vegetable_tools = ["土豆", "胡萝卜", "花菜", "白萝卜", "西葫芦", "番茄", "芹菜", "黄瓜", "洋葱", "莴笋", "菌菇", "茄子", "豆腐", "包菜", "白菜", "鸡蛋"]
        data = filter_vegetarian_recipes(vegetable_tools, data)

    for item in data:
        if 'stuff' in item:
            stuff_list = item['stuff']
            if all(ingredient in stuff_list for ingredient in process_emoji(target_list)):
                matching_items.append(item)

    return matching_items


# 菜品介绍
def describe_dish(dish):
    emoji_dict = {
        "土豆": "🥔", "胡萝卜": "🥕", "花菜": "🥦", "白萝卜": "🥣",
        "西葫芦": "🥒", "番茄": "🍅", "芹菜": "🥬", "黄瓜": "🥒",
        "洋葱": "🧅", "莴笋": "🎍", "菌菇": "🍄", "茄子": "🍆",
        "豆腐": "🍲", "包菜": "🥗", "白菜": "🥬",
        "面食": "🍝", "面包": "🍞", "米": "🍚", "方便面": "🍜",
        "午餐肉": "🥓", "香肠": "🌭", "腊肠": "🌭", "鸡肉": "🐤",
        "猪肉": "🐷", "鸡蛋": "🥚", "虾": "🦐", "牛肉": "🐮", "骨头": "🦴"
    }

    # 将食材的中文名称后面添加对应的emoji

    name = dish.get("name", "")
    bv = dish.get("bv", "暂无BV号")
    difficulty = dish.get("difficulty", None)
    tags = ", ".join(dish.get("tags", []))
    methods = ", ".join(dish.get("methods", []))
    tools = ", ".join(dish.get("tools", []))

    stuff: list = dish.get("stuff", [])

    stuff_emoji = []
    for ingredient in stuff:
        emoji = emoji_dict.get(ingredient)
        if emoji:
            stuff_emoji.append(f"{ingredient}{emoji}")
        else:
            stuff_emoji.append(f"{ingredient}")

    stuff_emoji = "、".join(stuff_emoji)

    description = f"灯灯也喜欢吃{name}✨，需要准备{stuff_emoji}。"
    if tools:
        description += f"要用{tools}"
        if methods and methods != '':
            description += f"{methods}"
        else:
            description += f"制作"
    if difficulty:
        description += f"，难度大概是「{difficulty}」（"
    else:
        description += f"。"
    if tags:
        description += f"tag大概是「{tags}」。"
    if bv:
        description += f"\n{bv}"
    return description


def filter_vegetarian_recipes(vegetables, data):
    vegetarian_recipes = []

    for recipe in data:
        # 检查每个食材是否都是素菜，假设素菜的列表叫vegetables
        is_vegetarian = all(ingredient in vegetables for ingredient in recipe["stuff"])

        if is_vegetarian:
            vegetarian_recipes.append(recipe)
            # print('添加')

    return vegetarian_recipes

# 把列表选的只剩蔬菜


# 把列表选的只剩纯蔬菜（无豆腐 鸡蛋）


def random_food(select_food, num):
    name_list = []
    if num <= len(select_food):
        random_selection = random.sample(select_food, num)
    else:
        random_selection = random.sample(select_food, len(select_food))
    for i in random_selection:
        name_list.append(i.get("name"))
    if name_list:
        return "唔，如果是ano酱的话，大概会喜欢" +"、".join(name_list) + "这样的吧。"
    else:
        return "不知道吃啥了喵"


def _all_food(select_food):
    name_list = []
    for i in select_food:
        name_list.append(i.get("name"))
    if name_list:
        rpl = "灯灯找到符合要求的菜谱有：\n" +"、".join(name_list) + "。\n\n查询教程请写菜品名，如：\n查菜谱 葱油黄瓜\n查菜谱 脆口黄瓜"
        rpl_img = ImageUtils.text2img(rpl, {"width": 1300})
        rpl = h.image(rpl_img)
        return rpl
    else:
        with open('./plugins/_cook/menu.png', 'rb') as file:
            image_data = file.read()
        return f"不知道吃啥了喵，看看别的组合吧～{h.image(image_data)}"


def select_by_name(name, material=None):
    with open('./plugins/_cook/data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    for item in data:
        def remove_text_in_parentheses(input_text):
            # 使用正则表达式匹配括号内的内容并替换为空字符串
            cleaned_text = re.sub(r'（[^（）]*）', '', input_text)
            return cleaned_text
        pure_name = remove_text_in_parentheses(item.get("name"))
        if pure_name == name:
            return describe_dish(item)
    return ''


# print(random_food(select_by_stuff([]), 3))  # 吃什么
# print(all_food(select_by_stuff(['🐷', '🥔'])))  # 查菜谱
# print(select_by_name('干锅土豆五花肉'))  # 查菜谱




