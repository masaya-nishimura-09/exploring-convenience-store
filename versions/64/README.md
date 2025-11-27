# 64

## 概要

- 並列 Q 更新法
- python
- atm -> water(lemon or plain) -> register
- アイテムの判別を写真で行う
- Map1 を使用
- Y = 0.01
- 商品にそれぞれランダムな値段をつける
- レジで会計し、所持金が足りなければ買わない
- shopping_list にカテゴリを追加
- ユーザの設定ファイル(./input/config.json)を追加
- 商品の選択基準を設定ファイルで調整可能(prefer_lower_price_items)
- prefer_lower_price_items = true で実行
- 水はそれぞれ一つずつ(x, y)

## 実行方法

- $ python3 -m venv venv
- $ source venv/bin/activate
- $ pip install colorgram.py
- $ ./bash/delete_output.sh
- $ ./bash/reset.sh
- 同カテゴリで最安値の商品を優先するときは、./config.json の prefer_lower_price_items を true にする。最初に見つけた商品を優先するときは false にする。
- $ ./bash/df_execution.sh
