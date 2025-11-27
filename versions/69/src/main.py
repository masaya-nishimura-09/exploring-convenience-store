import random
from status import Status, Position, Wallet, ShoppingCart
from shopper import Shopper
from io_utils import load_config, create_output_file, get_q_map, get_map, get_shopping_list, show_progress_steps, output_results, save_q_map

# 1, 設定ファイルからパラメータを取得
config = load_config()

# 2, 出力用ファイル準備
output_file_path = create_output_file(config["version"])

# 3, 地図を読み込む
store_map = get_map(config["vertical"])

# 4, 買い物リストを読み込む
shopping_list = get_shopping_list()

# 5, Qマップを取得
q_map = get_q_map(config["item_amount"], config["vertical"])

# 6, ステータスの初期化
position = Position(config["starting_x"], config["starting_y"], config["vertical"], config["horizontal"])
wallet = Wallet(random.randint(0, 100000))
shopping_cart = ShoppingCart(config["item_amount"])
status = Status(
    position=position,
    wallet=wallet,
    shopping_cart=shopping_cart,
    shopping_list=shopping_list,
    q_map=q_map,
    epsilon=config["epsilon"],
    show_output=config["show_output"],
    store_map=store_map
)

# 7, Shopperの初期化
shopper = Shopper(status)

# 8, 歩く(メインループ)
with open(output_file_path, "a") as file:
    while status.shopping_cart.progress < status.shopping_cart.item_amount:
        shopper.walk(file)
        show_progress_steps(status)

# 9, 会計
shopper.checkout()

# 10, 最終結果出力
output_results(status, output_file_path)

# 11, Qマップを保存
save_q_map(status, config["item_amount"])
