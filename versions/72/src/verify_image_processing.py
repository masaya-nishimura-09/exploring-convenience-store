from correct_image_mapping import correct_image_mapping
from io_utils import write_image_processing_result


def verify_image_processing(shopping_cart):
    for item in shopping_cart:
        cart_item_name = item["name"]
        cart_item_symbol = item["symbol"]

        for row in correct_image_mapping:
            if row["name"] == cart_item_name and row["symbol"] != cart_item_symbol:
                write_image_processing_result(row["name"], row["symbol"], cart_item_name, cart_item_symbol)
