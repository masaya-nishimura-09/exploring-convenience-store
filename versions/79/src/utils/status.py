# 状態管理クラス群


# 全体状態管理クラス
class Status:
    def __init__(
        self,
        position,
        show_output,
        store_map,
    ):
        self.position = position
        self.show_output = show_output
        self.store_map = store_map
        self.people = []


# 位置情報管理クラス
class Position:
    def __init__(self, vertical, horizontal):
        self.vertical = vertical
        self.horizontal = horizontal
