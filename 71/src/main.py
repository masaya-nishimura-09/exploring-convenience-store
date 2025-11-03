from io_utils import get_shopping_list, get_store_items
from color_utils import compute_similarities
from write_csv import write_csv
from create_graph import create_graph

# # 1, 買い物リストを読み込む
# shopping_list = get_shopping_list()

# # 2, 店内商品リストを読み込む
# store_items = get_store_items()

# # 3, 店内商品と買い物リストの類似度を計算
# results = compute_similarities(shopping_list, store_items)

# # 4, 結果を書き出す
# write_csv(results)

# 5, 類似度グラフを作成
create_graph()
