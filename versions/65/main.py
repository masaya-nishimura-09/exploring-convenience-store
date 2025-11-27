import datetime
import random
import colorgram
import os
from operator import itemgetter
import json

VERTICAL = 20
HORIZONTAL = 50
ITEM_AMOUNT = 3
VERSION = 65
color_cache = {}


class Status:
    def __init__(self, x, y, initial_money, shopping_list, cart, finished_categories, epsilon, q, map, prefer_lower_price_items):
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
        self.q = q
        self.map = map
        self.prefer_lower_price_items = prefer_lower_price_items


def price_comparison(status, item, category): # 最安値か判別
    for s in status.shopping_list[category]:
        if s['id'] != item['id'] and s['price'] < item['price']: 
            return False
        
    return True


def write_price_list(status, item, category): # 買い物リストに見つけた商品の価格を記録。もしすべての商品の価格を記録した場合はTrueを返す
    is_price_list_filled = True
    for i in range(len(status.shopping_list[category])):
        if status.shopping_list[category][i]['id'] == item['id'] and status.shopping_list[category][i]['price'] == 0:
            status.shopping_list[category][i]['price'] = random_price()
        if status.shopping_list[category][i]['price'] == 0:
            is_price_list_filled = False

    return is_price_list_filled


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


def pick_item(status, item):
    item_rgb = color_picker(f"./input/item_images/{item}.jpg")
    item_name = ""
    item_price = 0
    category_name = ""

    found = False
    for category in status.shopping_list:
        for item in status.shopping_list[category]:
            rgb = item['rgb']
            if are_same_list(rgb, item_rgb):
                item_name = item['name']
                item_price = item['price']
                category_name = category
                found = True
                break
        if found:
            break

    for i in range(ITEM_AMOUNT):
        if status.cart[i] is None:
            status.cart[i] = {"name": item_name, "price": item_price}
            break

    for i in range(ITEM_AMOUNT):
        if status.finished_categories[i] is None:
            status.finished_categories[i] = category_name
            break

    return item_name


def item_checker(status, item_code): # 商品をかごに入れるべきか判別
    item_rgb = color_picker(f"./input/item_images/{item_code}.jpg")
    atm_rgb = status.shopping_list['atm'][0]['rgb']
    cashier_rgb = status.shopping_list['register'][0]['rgb']

    if status.progress == 0 and not are_same_list(item_rgb, atm_rgb):
        return False 

    if status.progress > 0 and are_same_list(item_rgb, atm_rgb):
        return False

    if status.progress < ITEM_AMOUNT - 1 and are_same_list(item_rgb, cashier_rgb):
        return False
        
    for category in status.shopping_list:
        for item in status.shopping_list[category]:
            rgb = item['rgb']

            if are_same_list(item_rgb, rgb):
                if any(f is not None and category == f for f in status.finished_categories): # もし同カテゴリ商品が買い物かごにあれば無視
                    return False
                if any(c is not None and item == c["name"] for c in status.cart): # もしその商品が買い物かごにあれば無視
                    return False
                if status.prefer_lower_price_items: # もし同カテゴリ内で最も安い商品を選ぶ場合
                    is_price_list_filled = write_price_list(status, item, category)
                    if is_price_list_filled:
                        is_this_cheapest = price_comparison(status, item, category)
                        if is_this_cheapest:
                            return True
                        else:
                            return False
                    else:
                        return False
                return True

    return False


def q_used_checker(item, cart): # 使用済みのＱマップか判別
    for c in cart:
        if c is not None:
            if c["name"] == item:
                return True
    return False


def q_comparison(status, next_direction):
    direction = next_direction
    value = 0

    if status.progress == 0:
        for i in range(4):
            if value < status.q[0][i][status.x][status.y]:
                value = status.q[0][i][status.x][status.y]
                direction = i

    if status.progress == ITEM_AMOUNT - 1:
        for i in range(4):
            if value < status.q[1][i][status.x][status.y]:
                value = status.q[1][i][status.x][status.y]
                direction = i

    if status.progress < ITEM_AMOUNT - 1 and status.progress > 0:
        for category in status.shopping_list:
            if category != "atm" and category != "register":
                is_q_used = False
                for item in status.shopping_list[category]:
                    if q_used_checker(item['name'], status.cart):
                        is_q_used = True
                if not is_q_used:
                    q_index = 2                    
                    for j in range(4):
                        if value < status.q[q_index][j][status.x][status.y]:
                            value = status.q[q_index][j][status.x][status.y]
                            direction = j
    if value == 0:
        direction = next_direction

    return direction

    
def is_random_walk(epsilon):
    return random.random() < epsilon


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

    if next_x >= 0 and next_y >= 0 and next_x < VERTICAL and next_y < HORIZONTAL:
        for i in range(ITEM_AMOUNT):
            if status.q[i][next_direction][status.x][status.y] > status.q[i][status.pd][status.px][status.py]:
                status.q[i][status.pd][status.px][status.py] = status.q[i][next_direction][status.x][status.y] * 0.9

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
        elif status.map[next_x][next_y] == '1':
            return status
        else:
            should_pick = item_checker(status, status.map[next_x][next_y])

            if should_pick == True:
                item_name = pick_item(status, status.map[next_x][next_y])
                status.progress = status.progress + 1

                if item_name == "atm":
                    status.q[0][next_direction][status.x][status.y] = 1000
                elif item_name == "register":
                    status.q[1][next_direction][status.x][status.y] = 1000
                elif item_name == "water":
                    status.q[2][next_direction][status.x][status.y] = 1000

            return status
    else:
        return status


# get current date and time
now = datetime.datetime.now()
date = datetime.date.today()
time = now.strftime("%H-%M-%S-%f")

# create output file
output_file_name = f"./output/{date}_{time}.txt"
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

# fetch shopping list
shopping_list_path = "./input/shopping_list"
shopping_list = { 
    "atm": [], 
    "register": [],
    "water": []
}
id = 0
for s in os.listdir(shopping_list_path):
    category_path = os.path.join(shopping_list_path, s)
    if os.path.isdir(category_path):
        for c in os.listdir(category_path):
            item_path = os.path.join(category_path, c)
            shopping_list[s].append({ 'id': id, 'name': c, 'price': 0, 'rgb': color_picker(item_path)})
            id += 1

# fetch map
map = []
with open("./input/map.txt") as map_file:
    for _ in range(VERTICAL):
        map.append(list(map_file.readline().rstrip('\n')))

# fetch Q value
q = []
for i in range(ITEM_AMOUNT):
    item_q = []
    for j in range(4):
        current_q = []
        with open(f"./input/q/{i}/q{j}.txt") as f:
            for _ in range(VERTICAL):
                current_q.append([float(v) for v in f.readline().split()])
        item_q.append(current_q)
    q.append(item_q)

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
status = Status(starting_x, starting_y, initial_money, shopping_list, cart, finished_categories, epsilon, q, map, prefer_lower_price_items)
with open(output_file_name, "a") as file:
    keep_going = True
    while(keep_going):
        status = walk(status, file)
        if status.progress == ITEM_AMOUNT:
            keep_going = False

status = checkout(status)

# output result
print(f"\nOutput: {date}_{time}.txt")

print(f"\nEpsilon: {epsilon}")

shopping_list_text = "Shopping List: "
for i in shopping_list:
    shopping_list_text += f"{i} -> "
print(shopping_list_text)

cart_text = "Cart: "
for i in status.cart:
    cart_text += f"{i['name']}: {i['price']} -> "
print(cart_text)

items_purchased_text = "Items purchased: "
for i in status.items_purchased:
    items_purchased_text += f"{i['name']}: {i['price']} -> "
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
for i in range(ITEM_AMOUNT):
    for j in range(4):
        with open(f"./input/q/{i}/q{j}.txt", "w") as f:
            for k in range(VERTICAL):
                line = " ".join(f"{status.q[i][j][k][l]:.3f}" for l in range(HORIZONTAL))
                f.write(line + "\n")