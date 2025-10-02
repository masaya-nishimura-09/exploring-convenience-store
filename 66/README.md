# 66

## 概要

| 設定 | 経路                              | Q 更新法      | パラメータ     | 商品判別   | 購入ルール                                   |
| ---- | --------------------------------- | ------------- | -------------- | ---------- | -------------------------------------------- |
| 66   | ATM → 水(x と y の 2 種類) → レジ | 並列 Q 更新法 | ε = 0.01, Map1 | 写真で判別 | 最安値商品のみ購入。所持金不足なら購入しない |

## 実行方法

- $ python3 -m venv venv
- $ source venv/bin/activate
- $ pip install colorgram.py
- $ ./bash/reset.sh
- 同カテゴリで最安値の商品を優先するときは、./config.json の prefer_lower_price_items を true にする。最初に見つけた商品を優先するときは false にする。
- $ ./bash/df_execution.sh
