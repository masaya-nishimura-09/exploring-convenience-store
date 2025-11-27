# 65

## 概要

| 設定 | 経路                                     | Q 更新法      | パラメータ     | 商品判別   | 購入ルール                                              |
| ---- | ---------------------------------------- | ------------- | -------------- | ---------- | ------------------------------------------------------- |
| 65   | atm -> water(lemon or plain) -> register | 並列 Q 更新法 | ε = 0.01, Map1 | 写真で判別 | カテゴリを追加。prefer_lower_price_items = false で実行 |

## 実行方法

- $ python3 -m venv venv
- $ source venv/bin/activate
- $ pip install colorgram.py
- $ ./bash/delete_output.sh
- $ ./bash/reset.sh
- 同カテゴリで最安値の商品を優先するときは、./config.json の prefer_lower_price_items を true にする。最初に見つけた商品を優先するときは false にする。
- $ ./bash/df_execution.sh
