# 状態管理クラス群


# 全体状態管理クラス
class Status:
    def __init__(self, position, wallet, shopping_cart, shopping_list, q_map, epsilon, show_output, store_map):
        self.position = position
        self.wallet = wallet
        self.shopping_cart = shopping_cart
        self.shopping_list = shopping_list
        self.q_map = q_map
        self.epsilon = epsilon
        self.show_output = show_output
        self.store_map = store_map

    
    def give_max_q_value(self, item_id, direction):
        self.q_map[item_id][direction][self.position.x][self.position.y] = 1000


# 位置情報管理クラス
class Position:
    def __init__(self, x, y, vertical, horizontal):
        self.x = x
        self.y = y
        self.d = 0
        self.steps = 0
        self.prev_x = x
        self.prev_y = y
        self.prev_d = 0
        self.vertical = vertical
        self.horizontal = horizontal

    
    # 位置情報更新
    def move_to(self, x, y, d):
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = x
        self.y = y
        self.prev_d = d  
        self.steps += 1


# 所持金管理クラス
class Wallet:
    def __init__(self, initial_money):
        self.initial = initial_money
        self.balance = initial_money


# カート管理クラス
class ShoppingCart:
    def __init__(self, item_amount):
        self.item_amount = item_amount
        self.cart = [None] * item_amount
        self.items_purchased = []
        self.progress = 0
        self.is_shopping_successful = True

    
    def update_progress(self):
        self.progress += 1
