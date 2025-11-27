# 色取得ユーティリティ

import colorgram

_color_cache = {}


# 画像の色を取得しリスト化
def color_picker(path: str) -> list[str]:
    if path in _color_cache:
        return _color_cache[path]
    colors = colorgram.extract(path, 100)
    rgb_list = []
    for color in colors:
        rgb = color.rgb
        rgb_list.append(f"({rgb.r}, {rgb.g}, {rgb.b})")
    _color_cache[path] = rgb_list
    return rgb_list


# 2つのリスト(色)が同じか判別(順番も重複も無視)
def are_same_list(a, b):
    if set(a) == set(b):
        return True
    else:
        return False