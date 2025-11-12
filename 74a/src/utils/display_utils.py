import shutil
from utils.shopping_utils import *


# ターミナルの高さ分をリセット
def clear_terminal():
    terminal_height = shutil.get_terminal_size().lines
    print("\n" * terminal_height)


# ターミナルにマップと進捗を表示
def display_map(status, x, y):
    if status.show_output:
        # 画面クリア
        print("\033[H\033[J", end="")

        print("-" * 50)
        print()
        print(f"Map:")
        print("\n".join(status.store_map))
        print(
            f"\nProgress: {status.shopping_cart.progress}/{status.shopping_cart.item_amount}\n"
        )
        print(f"Steps: {status.position.steps}\n")
        print(f"Position: ({x}, {y})\n")
        print("Cart:")
        for i in status.shopping_cart.cart:
            if i is not None:
                print(
                    f"{{ Symbol: {i['symbol']}, Name: {i['name']}, Price: {i['price']}¥ }}"
                )


# 最終結果を出力
def display_results(status, output_file_path):
    if not status.show_output:
        pass

    shopping_list_str = get_shopping_list_str(status.shopping_list)
    cart_str = get_cart_str(status.shopping_cart.cart)
    items_purchased_str = get_items_purchased_str(status.shopping_cart.items_purchased)

    print(f"\nOutput file path: {output_file_path}\n")
    print(f"Epsilon: {status.epsilon}\n")
    print(shopping_list_str)
    print(cart_str)
    print(items_purchased_str)
    print(f"Initial money: {status.wallet.initial}¥\n")
    print(f"Cash balance: {status.wallet.balance}¥\n")
    print(f"Is shopping successful?: {status.shopping_cart.is_shopping_successful}\n")
    print(f"Progress: {status.shopping_cart.progress}\n")
    print(f"Steps: {status.position.steps}\n")
    clear_terminal()
