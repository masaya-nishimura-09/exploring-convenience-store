"""
3次元マップ化の実装例
このファイルは参考用のコード例です。実際の実装時に参考にしてください。
"""

import os
# 既存のモジュールから必要な関数をインポート（実装時に適切に修正）
# from utils.io_utils import get_root_dir
# from utils.shopping_utils import item_picked_checker, item_checker

# ============================================================================
# 1. Positionクラスの拡張例
# ============================================================================

class Position3D:
    """3次元位置情報管理クラス"""
    def __init__(self, x, y, z, vertical, horizontal, depth):
        self.x = x
        self.y = y
        self.z = z  # 新規追加: 0, 1, 2の3層
        self.d = 0
        self.steps = 0
        self.prev_x = x
        self.prev_y = y
        self.prev_z = z  # 新規追加
        self.prev_d = 0
        self.vertical = vertical
        self.horizontal = horizontal
        self.depth = depth  # 新規追加（通常は3）

    def move_to(self, x, y, z, d):
        """位置情報更新（z座標を追加）"""
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_z = self.z
        self.x = x
        self.y = y
        self.z = z
        self.prev_d = d
        self.steps += 1


# ============================================================================
# 2. 3Dマップデータの構造例
# ============================================================================

def create_3d_map_from_2d(map_data_2d, depth=3):
    """
    2Dマップを3Dマップに変換
    各階層は同じマップを使用（必要に応じて階層ごとに異なるマップも可能）
    """
    map_3d = []
    for z in range(depth):
        # 各階層に2Dマップをコピー
        map_3d.append([row[:] for row in map_data_2d])
    return map_3d


# 階層ごとに異なるマップを使用する場合の例
def create_custom_3d_map():
    """階層ごとに異なるマップを作成"""
    floor_0 = [
        "--        TDHEFVTGADQRIFIGKJABGQICLQQDHFQ         ",
        "--                                                ",
        # ... 1階のマップ
    ]
    floor_1 = [
        "--        ABCDEFGHIJKLMNOPQRSTUVWXYZ012345         ",
        "--                                                ",
        # ... 2階のマップ（商品配置が異なる）
    ]
    floor_2 = [
        "--        ZYXWVUTSRQPONMLKJIHGFEDCBA987654         ",
        "--                                                ",
        # ... 3階のマップ
    ]
    return [floor_0, floor_1, floor_2]


# ============================================================================
# 3. 移動方向の拡張（10方向）
# ============================================================================

def get_next_x_y_z(status, direction):
    """
    3D移動方向の計算
    方向: 0-7 = 水平8方向、8 = 上、9 = 下
    """
    next_x = status.position.x
    next_y = status.position.y
    next_z = status.position.z

    # 水平方向の移動（0-7: 既存の8方向）
    if direction == 0:  # 上
        next_x = status.position.x - 1
        next_y = status.position.y
    elif direction == 1:  # 右上
        next_x = status.position.x - 1
        next_y = status.position.y + 1
    elif direction == 2:  # 右
        next_x = status.position.x
        next_y = status.position.y + 1
    elif direction == 3:  # 右下
        next_x = status.position.x + 1
        next_y = status.position.y + 1
    elif direction == 4:  # 下
        next_x = status.position.x + 1
        next_y = status.position.y
    elif direction == 5:  # 左下
        next_x = status.position.x + 1
        next_y = status.position.y - 1
    elif direction == 6:  # 左
        next_x = status.position.x
        next_y = status.position.y - 1
    elif direction == 7:  # 左上
        next_x = status.position.x - 1
        next_y = status.position.y - 1
    # 垂直方向の移動
    elif direction == 8:  # 上に移動（z+1）
        next_z = min(status.position.z + 1, status.position.depth - 1)
    elif direction == 9:  # 下に移動（z-1）
        next_z = max(status.position.z - 1, 0)

    return next_x, next_y, next_z


# ============================================================================
# 4. 階段/エレベーターの実装例
# ============================================================================

def can_move_vertically(status, next_x, next_y, next_z):
    """
    垂直移動が可能かチェック
    階段やエレベーターの位置にいる場合のみ上下移動可能
    """
    # 階段の位置を定義（例）
    stairs_positions = [
        (5, 10, 0),  # 1階の階段
        (5, 10, 1),  # 2階の階段
        (5, 10, 2),  # 3階の階段
        (15, 25, 0),  # 別の階段（1階）
        (15, 25, 1),
        (15, 25, 2),
    ]

    # 現在位置または次の位置が階段の位置にあるかチェック
    current_pos = (status.position.x, status.position.y, status.position.z)
    next_pos = (next_x, next_y, next_z)

    # z座標が変化している場合、階段の位置にいる必要がある
    if status.position.z != next_z:
        return current_pos in stairs_positions or next_pos in stairs_positions

    return True  # 水平移動は常に可能


# ============================================================================
# 5. Qマップの3D化例
# ============================================================================

def get_q_map_3d(item_amount: int, vertical: int, horizontal: int, depth: int) -> list:
    """
    3D Qマップを取得
    構造: q_map[item_id][direction][x][y][z]
    """
    q_map = []
    for i in range(item_amount):
        item_q = []
        for j in range(10):  # 10方向（8水平 + 2垂直）
            current_q = []
            # root_dir = get_root_dir()  # 既存のutils.io_utilsからインポート
            root_dir = ""  # 実装時に適切なパスを設定
            # ファイル名の例: input/q/{i}/q{j}_z{z}.txt または input/q/{i}/q{j}.txt（全層を含む）
            for z in range(depth):
                z_level = []
                # オプション1: 階層ごとにファイルを分ける
                file_path = os.path.join(root_dir, f"input/q/{i}/q{j}_z{z}.txt")
                if os.path.exists(file_path):
                    with open(file_path) as f:
                        for _ in range(vertical):
                            z_level.append([float(v) for v in f.readline().split()])
                else:
                    # オプション2: 1ファイルに全階層を含む場合
                    # ファイル構造: 最初のvertical行がz=0、次のvertical行がz=1、...
                    file_path = os.path.join(root_dir, f"input/q/{i}/q{j}.txt")
                    with open(file_path) as f:
                        # z層の開始行を計算
                        start_line = z * vertical
                        for line_num, line in enumerate(f):
                            if start_line <= line_num < start_line + vertical:
                                z_level.append([float(v) for v in line.split()])
                current_q.append(z_level)
            item_q.append(current_q)
        q_map.append(item_q)
    return q_map


def save_q_map_3d(status, item_amount):
    """3D Qマップを保存"""
    for i in range(item_amount):
        for j in range(10):  # 10方向
            # root_dir = get_root_dir()  # 既存のutils.io_utilsからインポート
            root_dir = ""  # 実装時に適切なパスを設定
            # 階層ごとにファイルを分ける場合
            for z in range(status.position.depth):
                file_path = os.path.join(root_dir, f"input/q/{i}/q{j}_z{z}.txt")
                with open(file_path, "w") as f:
                    for x in range(status.position.vertical):
                        line = " ".join(
                            f"{status.q_map[i][j][x][y][z]:.3f}"
                            for y in range(status.position.horizontal)
                        )
                        f.write(line + "\n")


# ============================================================================
# 6. Qマップ比較の3D化例
# ============================================================================

def q_comparison_3d(status, next_direction):
    """3D Qマップを比較し、次の方向を決める"""
    direction = next_direction
    value = 0

    # 買い物リストからatmとレジのidを取得（既存のロジック）
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

    x, y, z = status.position.x, status.position.y, status.position.z

    # まだatmを探している時
    if status.shopping_cart.progress == 0:
        for i in range(10):  # 10方向
            q_value = status.q_map[atm_index][i][x][y][z]
            if value < q_value:
                value = q_value
                direction = i

    # レジを探している時
    elif status.shopping_cart.progress == status.shopping_cart.item_amount - 1:
        for i in range(10):
            q_value = status.q_map[cashier_index][i][x][y][z]
            if value < q_value:
                value = q_value
                direction = i

    # 商品を探している時
    else:
        for i in range(status.shopping_cart.item_amount):
            if i != atm_index and i != cashier_index:
                is_item_picked = item_picked_checker(
                    status.shopping_list[i]["name"], status.shopping_cart.cart
                )
                if not is_item_picked:
                    for j in range(10):
                        q_value = status.q_map[i][j][x][y][z]
                        if value < q_value:
                            value = q_value
                            direction = j

    if value == 0:
        direction = next_direction

    return direction


# ============================================================================
# 7. Qマップ更新の3D化例
# ============================================================================

def update_all_q_map_3d(status, next_direction):
    """3D Qマップを更新"""
    x, y, z = status.position.x, status.position.y, status.position.z
    prev_x, prev_y, prev_z = (
        status.position.prev_x,
        status.position.prev_y,
        status.position.prev_z,
    )

    for i in range(len(status.shopping_list)):
        current_q = status.q_map[i][next_direction][x][y][z]
        prev_q = status.q_map[i][status.position.prev_d][prev_x][prev_y][prev_z]

        if current_q > prev_q:
            status.q_map[i][status.position.prev_d][prev_x][prev_y][prev_z] = (
                current_q * 0.9
            )


# ============================================================================
# 8. マップアクセスの変更例
# ============================================================================

def get_tile_3d(store_map, x, y, z):
    """3Dマップからタイルを取得"""
    return store_map[z][x][y]


# ============================================================================
# 9. 表示の改善例
# ============================================================================

def display_map_3d(status, x, y, z):
    """3Dマップを表示"""
    if status.show_output:
        print("\033[H\033[J", end="")  # 画面クリア

        print("-" * 50)
        print()
        print(f"Current Floor: {z}")
        print(f"Map:")
        # 現在の階層のマップを表示
        print("\n".join(status.store_map[z]))
        print(
            f"\nProgress: {status.shopping_cart.progress}/{status.shopping_cart.item_amount}\n"
        )
        print(f"Steps: {status.position.steps}\n")
        print(f"Position: ({x}, {y}, {z})\n")  # z座標を追加
        print("Cart:")
        for i in status.shopping_cart.cart:
            if i is not None:
                print(
                    f"{{ Symbol: {i['symbol']}, Name: {i['name']}, Price: {i['price']}¥ }}"
                )


# ============================================================================
# 10. Shopperクラスのwalkメソッドの変更例
# ============================================================================

def walk_3d_example(self, file):
    """3D対応のwalkメソッド例"""
    status = self.status

    next_direction = get_next_direction(status)  # 10方向から選択
    next_x, next_y, next_z = get_next_x_y_z(status, next_direction)

    # 範囲チェック（z座標を追加）
    if not (
        next_x >= 0
        and next_y >= 0
        and next_z >= 0
        and next_x < status.position.vertical
        and next_y < status.position.horizontal
        and next_z < status.position.depth
    ):
        return

    # 垂直移動のチェック（階段の位置にいる必要がある）
    if status.position.z != next_z:
        if not can_move_vertically(status, next_x, next_y, next_z):
            return

    # 3Dマップからタイルを取得
    next_tile = status.store_map[next_z][next_x][next_y]

    # Qマップを更新
    update_all_q_map_3d(status, next_direction)

    # 次の場所が通行可能なマスのとき
    if next_tile == " " or next_tile == "*":
        # マップを更新
        row = list(status.store_map[next_z][next_x])
        row[next_y] = "*"
        status.store_map[next_z][next_x] = "".join(row)

        # 位置情報更新（z座標を追加）
        status.position.move_to(next_x, next_y, next_z, next_direction)

        # ターミナルにマップを表示
        display_map_3d(status, next_x, next_y, next_z)

        # 出力ファイルに書き込み（z座標を追加）
        write_position_to_file_3d(file, next_x, next_y, next_z)
        return

    # 次の場所がスタート地点のとき
    elif status.store_map[next_z][next_x][next_y] == "1":
        return

    # 次の場所に商品がある時
    else:
        true_or_false, item_id = item_checker(status, next_tile)
        if true_or_false:
            status.shopping_cart.update_progress()
            status.give_max_q_value_3d(item_id, next_direction)
        return


def write_position_to_file_3d(file, x, y, z):
    """3D位置情報をファイルに書き込み"""
    file.write(f"({x}, {y}, {z})\n")


def give_max_q_value_3d(self, item_id, direction):
    """3D Qマップに最大値を設定"""
    x, y, z = self.position.x, self.position.y, self.position.z
    self.q_map[item_id][direction][x][y][z] = 1000

