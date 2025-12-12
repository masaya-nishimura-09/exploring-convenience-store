import random
from utils.status import Status, Position, Wallet, ShoppingCart
from models.shopper import Shopper
from utils.io_utils import (
    load_config,
    create_output_file,
    write_results,
)
from utils.shopping_utils import (
    get_shopping_list,
    get_shopping_list_str,
    get_cart_str,
    get_items_purchased_str,
)
from utils.q_map_utils import get_q_map, save_q_map
from utils.display_utils import display_results
from utils.image_utils import verify_image_processing
from libs.map import map_data


def main():
    # 1, 設定ファイルからパラメータを取得
    config = load_config()

    # 2, 出力用ファイル準備
    output_file_path = create_output_file(config["version"])

    # 3, 地図を読み込む
    store_map = map_data

    # 4, 買い物リストを読み込む
    shopping_list = get_shopping_list()

    # 5, Qマップを取得
    q_map = get_q_map(config["item_amount"], config["vertical"])

    # 6, ステータスの初期化
    position = Position(
        config["starting_x"],
        config["starting_y"],
        config["vertical"],
        config["horizontal"],
        config["max_step"],
    )
    wallet = Wallet(random.randint(0, 100000))
    shopping_cart = ShoppingCart(config["item_amount"], config["similarity_threshold"])
    status = Status(
        position=position,
        wallet=wallet,
        shopping_cart=shopping_cart,
        shopping_list=shopping_list,
        q_map=q_map,
        epsilon=config["epsilon"],
        show_output=config["show_output"],
        store_map=store_map,
    )

    # 7, Shopperの初期化
    shopper = Shopper(status)

    # 8, 歩く(メインループ)
    with open(output_file_path, "a") as file:
        while status.shopping_cart.progress < status.shopping_cart.item_amount:
            shopper.walk(file)

    # 9, 会計
    shopper.checkout()

    # 10, 最終結果出力
    shopping_list_str = get_shopping_list_str(status.shopping_list)
    cart_str = get_cart_str(status.shopping_cart.cart)
    items_purchased_str = get_items_purchased_str(status.shopping_cart.items_purchased)

    write_results(
        status, output_file_path, shopping_list_str, cart_str, items_purchased_str
    )
    display_results(
        status, output_file_path, shopping_list_str, cart_str, items_purchased_str
    )

    # 11, Qマップを保存
    save_q_map(status, config["item_amount"])

    # 12, 画像認識の正確性を評価
    verify_image_processing(status.shopping_cart.cart)


if __name__ == "__main__":
    main()
