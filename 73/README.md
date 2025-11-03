# 73

## 概要

| 設定 | 経路                                               | Q 更新法      | パラメータ                               | 商品判別   | 購入ルール                                   | 追加事項                                                                      |
| ---- | -------------------------------------------------- | ------------- | ---------------------------------------- | ---------- | -------------------------------------------- | ----------------------------------------------------------------------------- |
| 73   | ATM → 飲み物、朝食、ペンをそれぞれ 1 つずつ → レジ | 並列 Q 更新法 | ε = 0.01, Map1, similarity_threshold=0.7 | 写真で判別 | 最安値商品のみ購入。所持金不足なら購入しない | 同じ商品には同じ写真を使用。また、71 の結果による最適類似度パラメータを使用。 |

## 設定ファイルについて(./input/config.json)

- version: このプロジェクトの番号
- item_amount: ./input/shopping_list 内の写真の枚数（実行後に自動作成）
- epsilon: ε の値
- starting_x: 開始地点の x 座標
- starting_y: 開始地点の y 座標
- prefer_lower_price_items: 各カテゴリの最安値の商品をそれぞれ購入する場合は true、先に見つけたものを購入する場合は false (現時点では true のみ可能)
- show_output:結果を都度ターミナルに出力するときは true
- similarity_threshold: 類似度のしきい値
- title: 実験の手法
- runs_per_set: 1 セットあたりの実行回数,
- sets: セット数

## 実行方法

- $ python3 -m venv venv
- $ source venv/bin/activate
- $ pip install torch torchvision pillow matplotlib
- $ ./execution.sh
