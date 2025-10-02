import datetime
import random
import colorgram
import os
from operator import itemgetter
import json

VERTICAL = 20
HORIZONTAL = 50
ITEM_AMOUNT = 4
CATEGORY_AMOUNT = 3
VERSION = 66
color_cache = {}


class Status:
    def __init__(self, x, y, initial_money, shopping_list, cart, finished_categories, epsilon, map, prefer_lower_price_items):
        self.x = x
        self.y = y
        self.d = 0
        self.steps = 0
        self.px = x
        self.py = y
        self.pd = 0
        self.progress = 0
        self.initial_money = initial_money
        self.cash_balance = initial_money
        self.is_shopping_successful = True
        self.shopping_list = shopping_list
        self.cart = cart
        self.finished_categories = finished_categories
        self.items_purchased = []
        self.epsilon = epsilon
        self.map = map
        self.prefer_lower_price_items = prefer_lower_price_items


def price_comparison(status, item, category): # 最安値か判別
    for s in status.shopping_list[category]:
        if s['id'] != item['id'] and s['price'] < item['price']: 
            return False
    return True


# 買い物リストに見つけた商品の価格を記録
def write_price_list(status, item, category):
    if category == "atm" or category == "register":
        return
    for i in range(len(status.shopping_list[category])):
        if status.shopping_list[category][i]['id'] == item['id'] and status.shopping_list[category][i]['price'] == 0:
            status.shopping_list[category][i]['price'] = random_price()
    return


def checkout(status):
    cart = [item for item in status.cart if item["name"] != "atm.jpg" and item["name"] != "cashier_register.jpg"]
    sorted_cart = sorted(cart, key=itemgetter("price"))
    for item in sorted_cart:
        if item["price"] <= status.cash_balance:
            status.items_purchased.append({"name": item["name"], "price": item["price"]})
            status.cash_balance = status.cash_balance - item["price"]
        else:
            status.is_shopping_successful = False
            break
    return status


def random_price():
    price = random.randint(100, 10000)
    return price


def are_same_list(a, b):
    if set(a) == set(b):
        return True
    else:
        return False


def color_picker(path):
    if path in color_cache:
        return color_cache[path]
    colors = colorgram.extract(path, 100)
    rgb_list = []
    for color in colors:
        rgb = color.rgb
        rgb_list.append(f"({rgb.r}, {rgb.g}, {rgb.b})")
    color_cache[path] = rgb_list
    return rgb_list


# 商品をカゴに入れる
def pick_item(status, item):
    item_rgb = color_picker(f"./input/item_images/{item}.jpg")
    item_id = 0
    item_name = ""
    item_price = 0
    category_name = ""
    is_category_finished = False

    # 商品の詳細を取得
    found = False
    for category in status.shopping_list:
        for item in status.shopping_list[category]:
            rgb = item['rgb']
            if are_same_list(rgb, item_rgb):
                item_id = item['id']
                item_name = item['name']
                item_price = item['price']
                category_name = category
                found = True
                break
        if found:
            break

    # カゴに商品を追加
    for i in range(ITEM_AMOUNT):
        if status.cart[i] is None:
            status.cart[i] = {"id": item_id, "category": category_name, "name": item_name, "price": item_price}
            break

    # カートの中の同カテゴリの商品数と買い物リストの同カテゴリの商品数を比較
    cart_count = sum(1 for item in status.cart if item is not None and item["category"] == category_name)
    shopping_list_count = len(status.shopping_list[category_name])
    if cart_count == shopping_list_count:
        is_category_finished = True 

    if is_category_finished == True:
        # カテゴリを探索終了にする
        for i in range(ITEM_AMOUNT):
            if status.finished_categories[i] is None:
                status.finished_categories[i] = category_name
                break
        
    return item_id


# そのカテゴリのうち、必要な商品以外を削除
def delete_items_from_cart(status, item_id):
    category_name = ""
    lowest_price = float("inf") # 無限大

    # 1. item_id が属するカテゴリを探す
    for category in status.shopping_list:
        for item in status.shopping_list[category]:
            if item['id'] == item_id:
                category_name = category
                break
        if category_name:
            break
    
    # 2. そのカテゴリで最安の商品を探す
    for item in status.cart:
        if item is not None and item["category"] == category_name:
            if item["price"] < lowest_price:
                lowest_price = item["price"]

    # 3. カートから最安以外を削除
    new_cart = []
    kept = False
    for item in status.cart:
        if item is not None and item["category"] == category_name:
            if item["price"] == lowest_price and not kept:
                # 1つだけ残す
                new_cart.append(item)
                kept = True
        else:
            new_cart.append(item)
    status.cart = new_cart


# 商品をかごに入れるべきか判別
def item_checker(status, item_code): 
    item_rgb = color_picker(f"./input/item_images/{item_code}.jpg")
    atm_rgb = status.shopping_list['atm'][0]['rgb']
    cashier_rgb = status.shopping_list['register'][0]['rgb']

    # まだ何も見つけてない　かつ　見つけたものがatmでない時
    if status.progress == 0 and not are_same_list(item_rgb, atm_rgb):
        return False

    # atmを見つけた後　かつ　見つけたものがatmの時
    if status.progress > 0 and are_same_list(item_rgb, atm_rgb):
        return False

    # レジ以外に見つけてないものがある　かつ　見つけたものがレジの時
    if status.progress < CATEGORY_AMOUNT - 1 and are_same_list(item_rgb, cashier_rgb):
        return False
    
    for category in status.shopping_list:
        for item in status.shopping_list[category]:
            rgb = item['rgb']

            if are_same_list(item_rgb, rgb):
                # もしそのカテゴリの探索が終了していれば無視
                if any(f is not None and category == f for f in status.finished_categories):
                    return False
                
                # もしその商品が買い物かごにあれば無視
                if any(c is not None and item["name"] == c["name"] for c in status.cart): 
                    return False
                
                # もし同カテゴリ内で最も安い商品を選ぶ場合
                if status.prefer_lower_price_items:
                    write_price_list(status, item, category)
                return True

    return False


# 商品をすでにカゴに入れたか判別
def item_picked_checker(item, cart):
    for c in cart:
        if c is not None:
            if c["name"] == item:
                return True
    return False


# そのカテゴリーの探索を終了するべきか判別
def category_finished_checker(status, item_id):
    category_name = ""
    found = False
    for category in status.shopping_list:
        for item in status.shopping_list[category]:
            if item['id'] == item_id:
                category_name = category
                found = True
                break
        if found:
            break
    
    for category in status.finished_categories:
        if category == category_name:
            return True
    return False


# Qマップを比較し、次の方向を決める
def q_comparison(status, next_direction):
    direction = next_direction
    value = 0

    # まだatmを探している時
    if status.progress == 0:
        for i in range(4):
            if value < status.shopping_list["atm"][0]["q"][i][status.x][status.y]:
                value = status.shopping_list["atm"][0]["q"][i][status.x][status.y]
                direction = i

    # レジを探している時
    elif status.progress == CATEGORY_AMOUNT - 1:
        for i in range(4):
            if value < status.shopping_list["register"][0]["q"][i][status.x][status.y]:
                value = status.shopping_list["register"][0]["q"][i][status.x][status.y]
                direction = i

    # 商品を探している時
    else:
        for category in status.shopping_list:
            if category != "atm" and category != "register":
                is_item_picked = any(
                    item_picked_checker(item['name'], status.cart) 
                    for item in status.shopping_list[category]
                )
                if not is_item_picked:
                    for item in status.shopping_list[category]:
                        for i in range(4):
                            if value < item["q"][i][status.x][status.y]:
                                value = item["q"][i][status.x][status.y]
                                direction = i
    if value == 0:
        direction = next_direction

    return direction


def is_random_walk(epsilon):
    return random.random() < epsilon


# qマップをリストに変換
def fetch_q_map(q_path):
    q = []
    for i in range(4):
        current_q = []
        with open(f"{q_path}/q{i}.txt") as f:
            for _ in range(VERTICAL):
                current_q.append([float(v) for v in f.readline().split()])
        q.append(current_q)
    return q


def walk(status, file):
    next_direction = random.randint(0, 3)
    random_walk = is_random_walk(status.epsilon)
    next_x = 0
    next_y = 0

    if random_walk == False:
        next_direction = q_comparison(status, next_direction)

    if next_direction == 0:
        next_x = status.x - 1
        next_y = status.y
    elif next_direction == 1:
        next_x = status.x
        next_y = status.y + 1
    elif next_direction == 2:
        next_x = status.x + 1
        next_y = status.y
    else:
        next_x = status.x
        next_y = status.y - 1

    # 次の場所がマップの範囲内の時
    if next_x >= 0 and next_y >= 0 and next_x < VERTICAL and next_y < HORIZONTAL:

        # Qマップを全て更新する
        for category in status.shopping_list:
            for item in status.shopping_list[category]:
                if item["q"][next_direction][status.x][status.y] > item["q"][status.pd][status.x][status.y]:
                    item["q"][status.pd][status.x][status.y] = item["q"][next_direction][status.x][status.y] * 0.9

        # 次の場所が未通過か通過済みのとき
        if status.map[next_x][next_y] == ' ' or status.map[next_x][next_y] == '*':
            status.map[next_x][next_y] = '*'
            status.px = status.x
            status.py = status.y
            status.x = next_x
            status.y = next_y
            status.pd = next_direction
            status.steps = status.steps + 1

            print(f"({status.x}, {status.y})")
            file.write(f"({status.x}, {status.y})\n")

            return status
        
        # 次の場所がスタート地点のとき
        elif status.map[next_x][next_y] == '1':
            return status
        
        # 次の場所に商品がある時
        else:
            should_pick = item_checker(status, status.map[next_x][next_y])

            if should_pick == True:
                item_id = pick_item(status, status.map[next_x][next_y])

                if status.prefer_lower_price_items:
                    is_category_finished = category_finished_checker(status, item_id)
                    if is_category_finished == True:
                        delete_items_from_cart(status, item_id)
                        status.progress = status.progress + 1
                        for category in status.shopping_list:
                            for item in status.shopping_list[category]:
                                if item["id"] == item_id:
                                    item['q'][next_direction][status.x][status.y] = 1000
                else:
                    status.progress = status.progress + 1
                    for category in status.shopping_list:
                        for item in status.shopping_list[category]:
                            if item["id"] == item_id:
                                item['q'][next_direction][status.x][status.y] = 1000
                   
            return status
    else:
        return status


# get current date and time
now = datetime.datetime.now()
date = datetime.date.today()
time = now.strftime("%H-%M-%S-%f")

# create output file
output_file_name = f"./output/tmp_data/{date}_{time}.txt"
with open(output_file_name, "w") as file:
    file.write(f"{VERSION} output data\n\n")
    file.write("Passing Points:\n")

# fetch starting position
with open("./input/starting_position.txt") as starting_position_file:
    position = starting_position_file.readline().split(" ")
    starting_x = int(position[0])
    starting_y = int(position[1])

# fetch epsilon
with open("./input/epsilon.txt") as epsilon_file:
    epsilon = float(epsilon_file.readline())

# 買い物リスト及びそれぞれの商品のQマップを取得
shopping_list_path = "./input/shopping_list"
shopping_list = {}
id = 0
for category_name in os.listdir(shopping_list_path):
    category_path = os.path.join(shopping_list_path, category_name)
    shopping_list[category_name] = []

    for item_name in os.listdir(category_path):
        item_path = os.path.join(category_path, item_name)
        item_image_path = os.path.join(item_path, f'{item_name}.jpg')
        item_q_path = os.path.join(item_path, 'q')

        q = fetch_q_map(item_q_path)

        shopping_list[category_name].append({ 'id': id, 'name': item_name, 'price': 0, 'rgb': color_picker(item_image_path), 'q': q})
        id += 1

# fetch map
map = []
with open("./input/map.txt") as map_file:
    for _ in range(VERTICAL):
        map.append(list(map_file.readline().rstrip('\n')))

# read config json file
prefer_lower_price_items = False
with open('./input/config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    if data['prefer_lower_price_items'] == True:
        prefer_lower_price_items = True

# cart
cart = [None] * ITEM_AMOUNT

# finished categories
finished_categories = [None] * ITEM_AMOUNT

# initial money
initial_money = random.randint(0, 100000)

# walk
status = Status(starting_x, starting_y, initial_money, shopping_list, cart, finished_categories, epsilon, map, prefer_lower_price_items)
with open(output_file_name, "a") as file:
    keep_going = True
    while(keep_going):
        status = walk(status, file)
        print(f"Progress: {status.progress}, Steps: {status.steps}")
        if status.progress == CATEGORY_AMOUNT:
            keep_going = False
status = checkout(status)

# output result
print(f"\nOutput file name: {date}_{time}.txt")

print(f"Epsilon: {epsilon}")

shopping_list_text = "Shopping List: "
for i in shopping_list:
    shopping_list_text += f"{i} -> "
print(shopping_list_text)

cart_text = "Cart: "
for i in status.cart:
    if i is not None:
        cart_text += f"{i['name']}: {i['price']}¥ -> "
print(cart_text)

items_purchased_text = "Items purchased: "
for i in status.items_purchased:
    items_purchased_text += f"{i['name']}: {i['price']}¥ -> "
print(items_purchased_text)

print(f"Initial money: {status.initial_money}")

print(f"Cash balance: {status.cash_balance}")

print(f"Is shopping successful?: {status.is_shopping_successful}")

print(f"Progress: {status.progress}")

print(f"Steps: {status.steps}")

print(f"Map: ")
for i in range(VERTICAL):
    for j in range(HORIZONTAL):
        print(status.map[i][j], end="")
    print()

print()

with open(output_file_name, "a") as file:
    file.write(f"\nEpsilon: {epsilon}\n\n")
    file.write(f"{shopping_list_text}\n\n")
    file.write(f"{cart_text}\n\n")
    file.write(f"{items_purchased_text}\n\n")
    file.write(f"Initial money: {status.initial_money}\n\n")
    file.write(f"Cash balance: {status.cash_balance}\n\n")
    file.write(f"Is shopping successful?: {status.is_shopping_successful}\n\n")
    file.write(f"Progress: {status.progress}\n\n")
    file.write(f"Steps: {status.steps}\n\n")
    file.write(f"Map: \n")
    for i in range(VERTICAL):
        for j in range(HORIZONTAL):
            file.write(f"{status.map[i][j]}")
        file.write("\n")

# update Q value
for category in status.shopping_list:
    for item in status.shopping_list[category]:
        for j in range(4):
            q_dir = os.path.join(shopping_list_path, category, item['name'], 'q')
            q_file_path = os.path.join(q_dir, f"q{j}.txt")
            with open(q_file_path, "w") as f:
                for k in range(VERTICAL):
                    line = " ".join(f"{item['q'][j][k][l]:.3f}" for l in range(HORIZONTAL))
                    f.write(line + "\n")