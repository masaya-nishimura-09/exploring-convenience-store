# ファイル入出力ユーティリティ
import os


# プロジェクトのルートディレクトリのパスを取得
def get_root_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 買い物リスト（写真のパス）を取得
def get_shopping_list() -> list:
    root_dir = get_root_dir()
    shopping_list_path = os.path.join(root_dir, "images/shopping_list")
    shopping_list = []
    id = 0
    for item in os.listdir(shopping_list_path):
        shopping_list.append(
                {
                    "id": id,
                    "name": item.split(".")[0],
                    "path": os.path.join(shopping_list_path, item),
                    }
                )
        id += 1

    return shopping_list


# 店内商品リストを取得
def get_store_items() -> list:
    root_dir = get_root_dir()
    store_items_path = os.path.join(root_dir, "images/store_items")
    store_items = []
    id = 0
    for item in os.listdir(store_items_path):
        store_items.append(
                {
                    "id": id,
                    "name": item.split(".")[0],
                    "path": os.path.join(store_items_path, item),
                    }
                )
        id += 1

    return store_items
