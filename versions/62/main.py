import datetime
import random
import colorgram
import os
from operator import itemgetter

VERTICAL = 20
HORIZONTAL = 50
ITEM_AMOUNT = 5
VERSION = 62
color_cache = {}


class Status:
    def __init__(self, x, y, initial_money, shopping_list, cart, finished_categories, epsilon, q, map):
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


def pick_item(item, cart, finished_categories, shopping_list):
    item_rgb = color_picker(f"./input/item_images/{item}.jpg")
    item_name = ""
    category_name = ""

    found = False
    for category in shopping_list:
        for item in shopping_list[category]:
            full_path = f"./input/shopping_list/{category}/{item}"
            rgb = color_picker(full_path)
            if are_same_list(rgb, item_rgb):
                item_name = item
                category_name = category
                found = True
                break
        if found:
            break

    for i in range(ITEM_AMOUNT):
        if cart[i] == None:
            cart[i] = {"name": item_name, "price": random_price()}
            break

    for i in range(ITEM_AMOUNT):
        if finished_categories[i] == None:
            finished_categories[i] = category_name
            break

    return item_name


def item_checker(item, shopping_list, cart, finished_categories, progress):
    item_rgb = color_picker(f"./input/item_images/{item}.jpg")
    atm_rgb = color_picker(f"./input/shopping_list/atm/atm.jpg")
    cashier_rgb = color_picker(f"./input/shopping_list/register/cashier_register.jpg")

    if progress == 0 and not are_same_list(item_rgb, atm_rgb):
        return False 

    if progress > 0 and are_same_list(item_rgb, atm_rgb):
        return False

    if progress < ITEM_AMOUNT - 1 and are_same_list(item_rgb, cashier_rgb):
        return False
        
    for category in shopping_list:
        for item in shopping_list[category]:
            full_path = f"./input/shopping_list/{category}/{item}"
            rgb = color_picker(full_path)

            if are_same_list(item_rgb, rgb):
                if any(f is not None and category == f for f in finished_categories):
                    return False
                if any(c is not None and item == c["name"] for c in cart):
                    return False
                return True

    return False


def q_used_checker(item, cart):
    for c in cart:
        if c is not None:
            if c["name"] == item:
                return True
    return False


def q_comparison(q, status, next_direction, shopping_list, cart):
    direction = next_direction
    value = 0

    if status.progress == 0:
        for i in range(4):
            if value < q[0][i][status.x][status.y]:
                value = q[0][i][status.x][status.y]
                direction = i

    if status.progress == ITEM_AMOUNT - 1:
        for i in range(4):
            if value < q[1][i][status.x][status.y]:
                value = q[1][i][status.x][status.y]
                direction = i

    if status.progress < ITEM_AMOUNT - 1 and status.progress > 0:
        for key in shopping_list:
            if key != "atm" and key != "register":
                is_q_used = False
                for item in shopping_list[f"{key}"]:
                    if q_used_checker(item, cart):
                        is_q_used = True
                if not is_q_used:
                    q_index = 2
                    if key == 'pen':
                        q_index = 3
                    if key == 'drink':
                        q_index = 4
                    
                    for j in range(4):
                        if value < q[q_index][j][status.x][status.y]:
                            value = q[q_index][j][status.x][status.y]
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
        next_direction = q_comparison(status.q, status, next_direction, status.shopping_list, status.cart)

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
            should_pick = item_checker(status.map[next_x][next_y], status.shopping_list, status.cart, status.finished_categories, status.progress)
            if should_pick == True:
                item_name = pick_item(status.map[next_x][next_y], status.cart, status.finished_categories, status.shopping_list)
                status.progress = status.progress + 1

                if item_name == "atm":
                    status.q[0][next_direction][status.x][status.y] = 1000
                elif item_name == "register":
                    status.q[1][next_direction][status.x][status.y] = 1000
                elif item_name == "bento":
                    status.q[2][next_direction][status.x][status.y] = 1000
                elif item_name == "pen":
                    status.q[3][next_direction][status.x][status.y] = 1000
                elif item_name == "drink":
                    status.q[4][next_direction][status.x][status.y] = 1000

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
folder_path = "./input/shopping_list"
shopping_list = { 
    "atm": ["atm.jpg"], 
    "register": ["cashier_register.jpg"],
    "bento": [],
    "pen": [], 
    "water": []
}
for f in os.listdir(folder_path):
    full_path = os.path.join(folder_path, f)
    if os.path.isdir(full_path):
        for item in os.listdir(full_path):
            shopping_list[f"{f}"].append(item)

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

# cart
cart = [None] * ITEM_AMOUNT

# finished categories
finished_categories = [None] * ITEM_AMOUNT

# initial money
initial_money = random.randint(0, 100000)

# walk
status = Status(starting_x, starting_y, initial_money, shopping_list, cart, finished_categories, epsilon, q, map)
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