from typing import Union

# 想怎么导入都可以，你甚至可以把依赖直接写在这里


class H:

    @staticmethod
    def at(user_id: Union[int, str]):
        return f'<at id="{user_id}"/>'


h = H()

