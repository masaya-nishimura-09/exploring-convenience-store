import os
import random
from config_utils import *
from image_utils import calculate_similarity


# 買い物リスト（写真のパス）を取得
def get_shopping_list():
    shopping_list_path = os.path.join(get_root_dir(), "input/shopping_list")
    shopping_list = []
    id = 0
    for f in os.listdir(shopping_list_path):
        if f == "atm.jpg" or f == "cashier.jpg":
            shopping_list.append(
                {
                    "id": id,
                    "category": f.split(".")[0],
                    "name": f,
                    "path": os.path.join(shopping_list_path, f),
                }
            )
        else:
            shopping_list.append(
                {
                    "id": id,
                    "category": f.split("_")[0],
                    "name": f,
                    "path": os.path.join(shopping_list_path, f),
                }
            )
        id += 1

    return shopping_list


# 買い物リストを文字列で返す
def get_shopping_list_str(shopping_list):
    shopping_list_str = "Shopping List:\n"
    for i in shopping_list:
        shopping_list_str += f"- {i['name']}\n"
    return shopping_list_str


# カートの中身リストを文字列で返す
def get_cart_str(cart):
    cart_str = "Visit order:\n"
    order = 1
    for i in cart:
        if i is not None:
            cart_str += f"{order}, {{ Symbol: {i['symbol']}, Name: {i['name']}, Price: {i['price']}¥ }}\n"
            order += 1
    return cart_str


# 実際に購入した商品リストを文字列で変えす
def get_items_purchased_str(items_purchased):
    items_purchased_str = "Items purchased:\n"
    for i in items_purchased:
        items_purchased_str += f"{{{i['name']}: {i['price']}¥}}\n"
    return items_purchased_str


# 商品をかごに入れるべきか判別
def item_checker(status, tile):
    root_dir = get_root_dir()
    item_path = os.path.join(root_dir, f"input/item_images/{tile}.jpg")
    atm_path = next(
        (item["path"] for item in status.shopping_list if item["name"] == "atm.jpg"), ""
    )
    cashier_path = next(
        (
            item["path"]
            for item in status.shopping_list
            if item["name"] == "cashier.jpg"
        ),
        "",
    )

    # まだ何も見つけてない　かつ　見つけたものがatmでない時
    if status.shopping_cart.progress == 0 and not calculate_similarity(
        item_path, atm_path
    ):
        return False, 0

    # atmを見つけた後　かつ　見つけたものがatmの時
    if status.shopping_cart.progress > 0 and calculate_similarity(item_path, atm_path):
        return False, 0

    # レジ以外に見つけてないものがある　かつ　見つけたものがレジの時
    if status.shopping_cart.progress < len(
        status.shopping_list
    ) - 1 and calculate_similarity(item_path, cashier_path):
        return False, 0

    # 見つけた商品が買い物リストにある　かつ　まだカゴに入れてない時
    for s in status.shopping_list:
        if calculate_similarity(item_path, s["path"]):
            item_name = s["name"]
            if any(
                c is not None and item_name == c["name"]
                for c in status.shopping_cart.cart
            ):
                return False, 0

            pick_item(status, s, tile)
            return True, s["id"]

    return False, 0


# 商品をカゴに入れる
def pick_item(status, item, tile):
    price = 0
    if item["name"] == "atm.jpg" or item["name"] == "cashier.jpg":
        price = 0
    else:
        price = random.randint(100, 10000)

    # カゴに見つけた商品を入れる
    for i in range(len(status.shopping_list)):
        if status.shopping_cart.cart[i] == None:
            status.shopping_cart.cart[i] = {
                "category": item["category"],
                "symbol": tile,
                "name": item["name"],
                "price": price,
            }
            break


# 商品をすでにカゴに入れたか判別
def item_picked_checker(item, cart):
    for c in cart:
        if c is not None:
            if c["name"] == item:
                return True
    return False
