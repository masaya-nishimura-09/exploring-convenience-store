# 67

## 概要

| 設定 | 経路                                  | Q 更新法      | パラメータ     | 商品判別   | 購入ルール                                   |
| ---- | ------------------------------------- | ------------- | -------------- | ---------- | -------------------------------------------- |
| 67   | ATM → 水(2 種類), 弁当(2 種類) → レジ | 並列 Q 更新法 | ε = 0.01, Map1 | 写真で判別 | 最安値商品のみ購入。所持金不足なら購入しない |

## コードの流れ

- input から設定ファイルや q,地図を取得
- 買い物リストにある商品を全てカゴに入れる。
- checkout()でカゴの中を全て走査し、各カテゴリごとに最安値の 1 商品のみを購入する

## 設定ファイルについて(./input/config.json)

- version: このプロジェクトの番号
- item_amount: ./input/shopping_list 内の写真の枚数
- epsilon: ε の値
- starting_x: 開始地点の x 座標
- starting_y: 開始地点の y 座標
- prefer_lower_price_items: 各カテゴリの最安値の商品をそれぞれ購入する場合は true、先に見つけたものを購入する場合は false (現時点では true のみ可能)
- show_output:結果を都度ターミナルに出力するときは true

## 実行方法

- ./input/config.json を正しく設定する。
- 買い物リスト用の写真の名前は、`カテゴリ名_商品名.jpg` とする。(atm とレジは除く)
- 買い物リストの写真枚数に合わせて、q を用意する。(./fresh_stock/q と./input/q)
- $ python3 -m venv venv
- $ source venv/bin/activate
- $ pip install colorgram.py
- $ ./bash/reset.sh
- $ ./bash/df_execution.sh
  (このとき自動で./output 以下を作成)
- 全て終了後、 $ ./python3 graph.py
