import os
from utils.io_utils import get_root_dir
from utils.shopping_utils import item_picked_checker


# qマップを取得
def get_q_map(item_amount: int, vertical: int) -> list:
    q_map = []
    for i in range(item_amount):
        item_q = []
        for j in range(8):
            current_q = []
            root_dir = get_root_dir()
            with open(os.path.join(root_dir, f"input/q/{i}/q{j}.txt")) as f:
                for _ in range(vertical):
                    current_q.append([float(v) for v in f.readline().split()])
            item_q.append(current_q)
        q_map.append(item_q)
    return q_map


# 更新したqマップを保存
def save_q_map(status, item_amount):
    for i in range(item_amount):
        for j in range(8):
            root_dir = get_root_dir()
            with open(os.path.join(root_dir, f"input/q/{i}/q{j}.txt"), "w") as f:
                for k in range(status.position.vertical):
                    line = " ".join(
                        f"{status.q_map[i][j][k][l]:.3f}"
                        for l in range(status.position.horizontal)
                    )
                    f.write(line + "\n")


# Qマップを比較し、次の方向を決める
def q_comparison(status, next_direction):
    direction = next_direction
    value = 0

    # 買い物リストからatmとレジのidを取得
    atm_index = 0
    for item in status.shopping_list:
        if item["name"] == "atm.jpg":
            atm_index = item["id"]
            break

    cashier_index = 0
    for item in status.shopping_list:
        if item["name"] == "cashier.jpg":
            cashier_index = item["id"]
            break

    # まだatmを探している時
    if status.shopping_cart.progress == 0:
        for i in range(8):
            if value < status.q_map[atm_index][i][status.position.x][status.position.y]:
                value = status.q_map[atm_index][i][status.position.x][status.position.y]
                direction = i

    # レジを探している時
    elif status.shopping_cart.progress == status.shopping_cart.item_amount - 1:
        for i in range(8):
            if (
                value
                < status.q_map[cashier_index][i][status.position.x][status.position.y]
            ):
                value = status.q_map[cashier_index][i][status.position.x][
                    status.position.y
                ]
                direction = i

    # 商品を探している時
    else:
        for i in range(status.shopping_cart.item_amount):
            if i != atm_index and i != cashier_index:
                is_item_picked = item_picked_checker(
                    status.shopping_list[i]["name"], status.shopping_cart.cart
                )
                if not is_item_picked:
                    for j in range(8):
                        if (
                            value
                            < status.q_map[i][j][status.position.x][status.position.y]
                        ):
                            value = status.q_map[i][j][status.position.x][
                                status.position.y
                            ]
                            direction = j
    if value == 0:
        direction = next_direction

    return direction


# Qマップを更新
def update_all_q_map(status, next_direction):
    for i in range(len(status.shopping_list)):
        if (
            status.q_map[i][next_direction][status.position.x][status.position.y]
            > status.q_map[i][status.position.prev_d][status.position.prev_x][
                status.position.prev_y
            ]
        ):
            status.q_map[i][status.position.prev_d][status.position.prev_x][
                status.position.prev_y
            ] = (
                status.q_map[i][next_direction][status.position.x][status.position.y]
                * 0.9
            )


# 商品を見つけたときに最大のq値を与える
def give_max_q_value(status, item_id, next_direction):
        status.q_map[item_id][next_direction][status.position.x][status.position.y] = 1000
