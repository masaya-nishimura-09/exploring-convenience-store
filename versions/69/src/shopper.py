# 買い物エージェントのクラス

import os
import random
from q_learning import q_comparison, update_all_q_map
from io_utils import write_position_to_file, get_root_dir
from color_utils import color_picker, are_same_list
from operator import itemgetter


def get_next_direction(status):
    next_direction = random.randint(0, 7)
    is_random_walk = random.random() < status.epsilon

    if is_random_walk == False:
        next_direction = q_comparison(status, next_direction)
    return next_direction


def get_next_x_y(status, direction):
    next_x = 0
    next_y = 0

    if direction == 0:
        next_x = status.position.x - 1
        next_y = status.position.y
    elif direction == 1:
        next_x = status.position.x - 1
        next_y = status.position.y + 1
    elif direction == 2:
        next_x = status.position.x
        next_y = status.position.y + 1
    elif direction == 3:
        next_x = status.position.x + 1
        next_y = status.position.y + 1
    elif direction == 4:
        next_x = status.position.x + 1
        next_y = status.position.y
    elif direction == 5:
        next_x = status.position.x + 1
        next_y = status.position.y - 1
    elif direction == 6:
        next_x = status.position.x
        next_y = status.position.y - 1
    elif direction == 7:
        next_x = status.position.x - 1
        next_y = status.position.y - 1
    return next_x, next_y


# 商品をかごに入れるべきか判別
def item_checker(status, tile):
    root_dir = get_root_dir()
    # 対象の商品、atm、レジの色を取得
    item_rgb = color_picker(os.path.join(root_dir, f"input/item_images/{tile}.jpg") )

    atm_rgb = []
    for item in status.shopping_list:
        if item["name"] == "atm.jpg":
            atm_rgb = item["rgb"]
            break

    cashier_rgb = []
    for item in status.shopping_list:
        if item["name"] == "cashier_register.jpg":
            cashier_rgb = item["rgb"]
            break

    # まだ何も見つけてない　かつ　見つけたものがatmでない時
    if status.shopping_cart.progress == 0 and not are_same_list(item_rgb, atm_rgb):
        return False

    # atmを見つけた後　かつ　見つけたものがatmの時
    if status.shopping_cart.progress > 0 and are_same_list(item_rgb, atm_rgb):
        return False

    # レジ以外に見つけてないものがある　かつ　見つけたものがレジの時
    if status.shopping_cart.progress < len(status.shopping_list) - 1 and are_same_list(
        item_rgb, cashier_rgb
    ):
        return False

    # 見つけた商品が買い物リストにある　かつ　まだカゴに入れてない時
    for s in status.shopping_list:
        if are_same_list(item_rgb, s["rgb"]):
            item_name = s["name"]
            if any(c is not None and item_name == c["name"] for c in status.shopping_cart.cart):
                return False
            return True

    return False


# 商品をカゴに入れる
def pick_item(status, tile):
    root_dir = get_root_dir()
    item_rgb = color_picker(os.path.join(root_dir, f"input/item_images/{tile}.jpg") )

    item_id = 0
    item_name = ""
    item_category = ""

    price = 0
    if tile == "$" or tile == "-":
        price = 0
    else:
        price = random.randint(100, 10000)

    # 見つけた商品のid、名前、カテゴリを取得
    for item in status.shopping_list:
        if are_same_list(item["rgb"], item_rgb):
            item_id = item["id"]
            item_name = item["name"]
            item_category = item["category"]
            break

    # カゴに見つけた商品を入れる
    for i in range(len(status.shopping_list)):
        if status.shopping_cart.cart[i] == None:
            status.shopping_cart.cart[i] = {
                "category": item_category,
                "symbol": tile,
                "name": item_name,
                "price": price,
            }
            break

    return item_id


class Shopper:
    def __init__(self, status):
        self.status = status


    # 歩く
    def walk(self, file):
        status = self.status

        next_direction = get_next_direction(status)
        next_x, next_y = get_next_x_y(status, next_direction)

        # 次の場所がマップの範囲外の時は何もしない
        if not (next_x >= 0 and next_y >= 0 and next_x < status.position.vertical and next_y < status.position.horizontal):
            return
        
        next_tile = status.store_map[next_x][next_y]
        
        # Qマップを更新
        update_all_q_map(status, next_direction)

        # 次の場所が通行可能なマスのとき
        if next_tile == " " or next_tile == "*":

            # マップを更新
            status.store_map[next_x][next_y] = "*"

            # 位置情報更新
            status.position.move_to(next_x, next_y, next_direction)

            # 出力ファイルに書き込み+ターミナルに表示
            write_position_to_file(status.show_output, file, next_x, next_y)
            return

        # 次の場所がスタート地点のとき
        elif status.store_map[next_x][next_y] == "1":
            return

        # 次の場所に商品がある時
        else:
            if item_checker(status, next_tile):
                # カートに商品を入れ、idを取得
                item_id = pick_item(status, next_tile)

                # マップと進捗を更新
                status.shopping_cart.update_progress()
                status.give_max_q_value(item_id, next_direction)
            return
        

    # 会計をし、最安値の商品を購入
    def checkout(self):
        cart = [
            item
            for item in self.status.shopping_cart.cart
            if item is not None
            and item["name"] != "atm.jpg"
            and item["name"] != "cashier_register.jpg"
        ]

        # カートの中身を価格順にソート
        sorted_cart = sorted(cart, key=itemgetter("price"))

        # 購入したカテゴリリスト
        category_done = []

        # 所持金と相談しながら購入
        for item in sorted_cart:
            if item["category"] not in category_done:
                if item["price"] <= self.status.wallet.balance:
                    self.status.shopping_cart.items_purchased.append(
                        {"name": item["name"], "price": item["price"]}
                    )
                    self.status.wallet.balance = self.status.wallet.balance - item["price"]
                    category_done.append(item["category"])
                else:
                    self.status.shopping_cart.is_shopping_successful = False
                    break
