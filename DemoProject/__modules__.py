from modules.h import h

from modules.uni_manager import is_admin
from modules.uni_manager import auto_asset_path

from modules.logger import log

from modules.schedule_do import timer_do
from modules.schedule_do import interval_do

from modules.text_to_image import text2img

from modules.text_utils import escape_satori_special_characters
from modules.text_utils import unescape_satori_sspecial_characters
from modules.text_utils import plaintext_if_prefix
from modules.text_utils import remove_all_xml
from modules.text_utils import remove_first_prefix
from modules.text_utils import remove_all_at_xml
from modules.text_utils import remove_first_at_xml
from modules.text_utils import easy_to_show_text

from modules.command_matcher import match_command

# from modules.show_on import *  # 显示on类监听函数


# 想怎么导入都可以，你甚至可以把依赖直接写在这里

