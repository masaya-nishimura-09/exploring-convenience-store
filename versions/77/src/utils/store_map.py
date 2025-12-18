import string
import random


def replace_alphabets(string_list):
    new_string_list = []
    for row in string_list:
        new_row = ""
        for char in row:
            if char.isalpha():
                new_row += random.choice(string.ascii_uppercase)
            else:
                new_row += char
        new_string_list.append(new_row)
    return new_string_list


def create_store_map(first_floor, height):
    store_map = []
    for _ in range(height):
        floor = replace_alphabets(first_floor)
        store_map.append(floor)
    return store_map


def get_random_position(store_map, vertical, horizontal):
    x = 0
    y = 0

    while True:
        x = random.randrange(0, vertical)
        y = random.randrange(0, horizontal)

        if store_map[0][x][y] == " ":
            break
    return x, y


def reset_people(store_map, vertical, horizontal):
    for x in range(vertical):
        row = list(store_map[0][x])
        for y in range(horizontal):
            if row[y] == "!":
                row[y] = " "
        store_map[0][x] = "".join(row)


def move_people(status):
    vertical = status.position.vertical
    horizontal = status.position.horizontal
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    new_people = []
    for x, y in status.people:
        # 現在の位置をクリア
        row = list(status.store_map[0][x])
        if (x, y) in status.position.trajectory:
            row[y] = "*"
        else:
            row[y] = " "
        status.store_map[0][x] = "".join(row)

        # ランダムに方向を選ぶ
        dx, dy = random.choice(directions)
        nx, ny = x + dx, y + dy

        # 範囲内かチェック
        if 0 <= nx < vertical and 0 <= ny < horizontal:
            is_alphabet = status.store_map[0][nx][ny].isalpha()
            is_human = status.store_map[0][nx][ny] == "!"
            is_register = status.store_map[0][nx][ny] == "-"
            is_atm = status.store_map[0][nx][ny] == "$"
            is_start = status.store_map[0][nx][ny] == "1"

            if (
                not is_alphabet
                and not is_human
                and not is_register
                and not is_atm
                and not is_start
            ):
                # ロボットの位置でないかチェック
                if (nx, ny) != (status.position.x, status.position.y):
                    # 移動
                    row = list(status.store_map[0][nx])
                    row[ny] = "!"
                    status.store_map[0][nx] = "".join(row)
                    new_people.append((nx, ny))
                else:
                    # 移動せず、元の位置に戻す
                    row = list(status.store_map[0][x])
                    row[y] = "!"
                    status.store_map[0][x] = "".join(row)
                    new_people.append((x, y))
            else:
                # 移動せず、元の位置に戻す
                row = list(status.store_map[0][x])
                row[y] = "!"
                status.store_map[0][x] = "".join(row)
                new_people.append((x, y))
        else:
            # 移動せず、元の位置に戻す
            row = list(status.store_map[0][x])
            row[y] = "!"
            status.store_map[0][x] = "".join(row)
            new_people.append((x, y))

    status.people = new_people
