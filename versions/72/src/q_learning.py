# qマップ操作関数群


# 商品をすでにカゴに入れたか判別
def item_picked_checker(item, cart):
    for c in cart:
        if c is not None:
            if c["name"] == item:
                return True
    return False


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
            if value < status.q_map[cashier_index][i][status.position.x][status.position.y]:
                value = status.q_map[cashier_index][i][status.position.x][status.position.y]
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
                        if value < status.q_map[i][j][status.position.x][status.position.y]:
                            value = status.q_map[i][j][status.position.x][status.position.y]
                            direction = j
    if value == 0:
        direction = next_direction

    return direction


# Qマップを更新
def update_all_q_map(status, next_direction):
    for i in range(len(status.shopping_list)):
        if (
            status.q_map[i][next_direction][status.position.x][status.position.y]
            > status.q_map[i][status.position.prev_d][status.position.prev_x][status.position.prev_y]
        ):
            status.q_map[i][status.position.prev_d][status.position.prev_x][status.position.prev_y] = (
                status.q_map[i][next_direction][status.position.x][status.position.y] * 0.9
            )
