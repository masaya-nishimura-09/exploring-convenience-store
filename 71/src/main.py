import random
from status import Status, Position, Wallet, ShoppingCart
from io_utils import load_config, create_output_file, get_shopping_list

# 1, 買い物リストを読み込む
shopping_list = get_shopping_list()

print(shopping_list)
