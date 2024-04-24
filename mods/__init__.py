from core.event import Event
from core.on import on
from core.config import registers_manager, config
from core.log import log
from core.external import is_admin
from core.external import assets


from mods.h import h

from mods.schedule_do import timer_do
from mods.schedule_do import interval_do


from mods.command_matcher import match_command
from mods.command_matcher.text_utils import escape_satori_special_characters
from mods.command_matcher.text_utils import unescape_satori_special_characters
from mods.command_matcher.text_utils import plaintext_if_prefix
from mods.command_matcher.text_utils import remove_all_xml
from mods.command_matcher.text_utils import remove_first_prefix
from mods.command_matcher.text_utils import remove_all_at_xml
from mods.command_matcher.text_utils import remove_first_at_xml
from mods.command_matcher.text_utils import easy_to_show_text



