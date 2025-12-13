# 買い物エージェントのクラス

import random
from operator import itemgetter
from utils.io_utils import write_position_to_file
from utils.display_utils import display_map
from utils.q_map_utils import q_comparison, update_all_q_map, give_max_q_value, downgrade_q_map
from utils.shopping_utils import item_checker


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


class Shopper:
    def __init__(self, status):
        self.status = status

    # 歩く
    def walk(self, file):
        status = self.status

        next_direction = get_next_direction(status)
        next_x, next_y = get_next_x_y(status, next_direction)

        # 次の場所がマップの範囲外の時はqマップをダウングレード
        if not (
            next_x >= 0
            and next_y >= 0
            and next_x < status.position.vertical
            and next_y < status.position.horizontal
        ):
            downgrade_q_map(status, next_direction)
            return

        # 棚3層分の商品（アルファベット）を取得し、リスト化
        next_items = []
        for n in range(3):
            next_items.append(status.store_map[n][next_x][next_y])

        # Qマップを更新
        update_all_q_map(status, next_direction)

        # 次の場所が通行可能なマスのとき
        if next_items[0] == " " or next_items[0] == "*":

            # マップを更新
            row = list(status.store_map[0][next_x])
            row[next_y] = "*"
            status.store_map[0][next_x] = "".join(row)

            # 位置情報更新
            status.position.move_to(next_x, next_y, next_direction)

            # もし最大歩数に到達すると、レジに移動->進捗をレジの手前にする
            if status.position.steps >= status.position.max_step:
                status.position.go_to_register(status.shopping_cart.item_amount)

            # ターミナルにマップを表示
            display_map(status, next_x, next_y)

            # 出力ファイルに書き込み
            write_position_to_file(file, next_x, next_y)

            return

        # 次の場所がスタート地点のとき
        elif status.store_map[0][next_x][next_y] == "1":
            return

        # 次の場所に商品がある時
        else:
            true_or_false, item_id = item_checker(status, next_items)
            if true_or_false:

                # マップと進捗を更新
                status.shopping_cart.update_progress()
                give_max_q_value(status, item_id, next_direction)

            return


    # 会計をし、最安値の商品を購入
    def checkout(self):
        cart = [
            item
            for item in self.status.shopping_cart.cart
            if item is not None
            and item["name"] != "atm.jpg"
            and item["name"] != "cashier.jpg"
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
                    self.status.wallet.balance = (
                        self.status.wallet.balance - item["price"]
                    )
                    category_done.append(item["category"])
                else:
                    self.status.shopping_cart.is_shopping_successful = False
                    break
