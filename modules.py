from core.event import Event
from core.on import on
from core.config import registers_manager, config


from packages.h import h

from packages.uni_manager import is_admin
from packages.uni_manager import auto_asset_path

from packages.logger import log

from packages.schedule_do import timer_do
from packages.schedule_do import interval_do

from packages.text_to_image import text2img

from packages.text_utils import escape_satori_special_characters
from packages.text_utils import unescape_satori_sspecial_characters
from packages.text_utils import plaintext_if_prefix
from packages.text_utils import remove_all_xml
from packages.text_utils import remove_first_prefix
from packages.text_utils import remove_all_at_xml
from packages.text_utils import remove_first_at_xml
from packages.text_utils import easy_to_show_text

from packages.command_matcher import match_command

from packages.show_on import *  # 显示on类监听函数



