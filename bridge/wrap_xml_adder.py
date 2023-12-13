

from core.wrap_xml import H


class HExtension(H):
    @staticmethod
    def qq_passive(param: str):
        return f'<passive passiveId="{param}" />'


h = HExtension





