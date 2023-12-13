from config import admin_list, ban_dicts_path, config

from bridge.wrap_xml_adder import h
from bridge.decorator_maker import on_event, on_activator
from bridge.utils import rm_1_at, unescape_special_characters, escape_special_characters, rm_all_at, rm_all_xml, rm_perfix
from bridge.api_maker import new_api
from bridge.session_adder import SessionExtension, MessageExtension, Function










