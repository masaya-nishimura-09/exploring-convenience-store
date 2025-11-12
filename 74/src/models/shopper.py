from utils.q_map_utils import update_all_q_map
from utils.output_utils import write_position_to_file
from utils.store_map_utils import *
from utils.shopping_utils import *
from utils.display_utils import *
from operator import itemgetter


class Shopper:
    def __init__(self, status):
        self.status = status

    # 歩く
    def walk(self, file):
        status = self.status

        next_direction = get_next_direction(status)
        next_x, next_y = get_next_x_y(status, next_direction)

        # 次の場所がマップの範囲外の時は何もしない
        if not (
            next_x >= 0
            and next_y >= 0
            and next_x < status.position.vertical
            and next_y < status.position.horizontal
        ):
            return

        next_tile = status.store_map[next_x][next_y]

        # Qマップを更新
        update_all_q_map(status, next_direction)

        # 次の場所が通行可能なマスのとき
        if next_tile == " " or next_tile == "*":

            # マップを更新
            row = list(status.store_map[next_x])
            row[next_y] = "*"
            status.store_map[next_x] = "".join(row)

            # 位置情報更新
            status.position.move_to(next_x, next_y, next_direction)

            # ターミナルにマップを表示
            display_map(status, next_x, next_y)

            # 出力ファイルに書き込み
            write_position_to_file(status.show_output, file, next_x, next_y)
            return

        # 次の場所がスタート地点のとき
        elif status.store_map[next_x][next_y] == "1":
            return

        # 次の場所に商品がある時
        else:
            true_or_false, item_id = item_checker(status, next_tile)
            if true_or_false:

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
