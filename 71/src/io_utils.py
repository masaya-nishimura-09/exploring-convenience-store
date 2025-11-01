# ファイル入出力ユーティリティ

import os


# プロジェクトのルートディレクトリのパスを取得
def get_root_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 買い物リスト（写真のパス）を取得
def get_shopping_list() -> list:
    root_dir = get_root_dir()
    images_path = os.path.join(root_dir, "images")
    shopping_list = []
    id = 0
    for category in os.listdir(images_path):
        category_path = os.path.join(images_path, category)
        if not os.path.isdir(category_path):
            continue
        for item in os.listdir(category_path):
            shopping_list.append(
                {
                    "id": id,
                    "category": category,
                    "name": item.split(".")[0],
                    "path": os.path.join(category_path, item),
                }
            )
            id += 1

    return shopping_list


# 店内商品リストを取得
def get_store_items(shopping_list: list) -> list:
    store_items = []
    for item in shopping_list:
        if "_a" in item["name"]:
            store_items.append(item)
    return store_items
