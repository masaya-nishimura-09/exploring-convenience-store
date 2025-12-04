# プロジェクト評価レポート

## 1. Q 学習としての評価

### 1.1 標準的な Q 学習との比較

このプロジェクトは**Q 学習の変形版**として実装されていますが、標準的な Q 学習とは以下の点で異なります：

#### 標準的な Q 学習の更新式

```
Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
```

- `α`: 学習率
- `r`: 即時報酬
- `γ`: 割引率
- `s'`: 次の状態
- `a'`: 次の状態での最適行動

#### 本プロジェクトの更新式（`update_all_q_map`関数）

```97:110:src/utils/q_map_utils.py
# Qマップを更新
def update_all_q_map(status, next_direction):
    for i in range(len(status.shopping_list)):
        if (
            status.q_map[i][next_direction][status.position.x][status.position.y]
            > status.q_map[i][status.position.prev_d][status.position.prev_x][
                status.position.prev_y
            ]
        ):
            status.q_map[i][status.position.prev_d][status.position.prev_x][
                status.position.prev_y
            ] = (
                status.q_map[i][next_direction][status.position.x][status.position.y]
                * 0.9
            )
```

**主な違い：**

1. **条件付き更新**: 次の状態の Q 値が前の状態の Q 値より大きい場合のみ更新
2. **更新方向の逆転**: 通常は `Q(prev) ← f(Q(next))` だが、本実装は逆方向の更新
3. **報酬の扱い**: 即時報酬 `r` が更新式に含まれていない
4. **並列更新**: すべての商品アイテム（`i`）に対して同時に Q 値を更新

### 1.2 報酬の実装

報酬は商品発見時に設定されます：

```17:18:src/utils/status.py
    def give_max_q_value(self, item_id, direction):
        self.q_map[item_id][direction][self.position.x][self.position.y] = 1000
```

これは**スパース報酬**（稀にしか与えられない報酬）として機能しています。

### 1.3 結論：Q 学習と呼べるか？

**部分的に Q 学習と呼べますが、より正確には「Q 学習にインスパイアされた独自の強化学習アルゴリズム」です。**

理由：

- ✅ Q 値テーブルを使用
- ✅ ε-greedy 方策を使用（`epsilon = 0.01`）
- ✅ 価値関数の更新を行う
- ❌ 標準的な Q 学習の更新式を使用していない
- ❌ 報酬が更新式に直接組み込まれていない
- ✅ 独自の「並列 Q 更新法」を実装

## 2. 独自アルゴリズムの特徴

### 2.1 並列 Q 更新法（Parallel Q Update Method）

本プロジェクトの核心となる独自のアルゴリズムです：

**特徴：**

1. **複数目標の同時学習**: 各商品アイテムごとに独立した Q マップを保持
2. **条件付き更新**: `Q(next) > Q(prev)` の時のみ更新（価値の増加を伝播）
3. **割引係数 0.9**: 次の状態の Q 値の 90%を前の状態に伝播
4. **逆方向伝播**: 通常の Q 学習とは逆方向に価値を伝播させる

**動作の流れ：**

```
1. エージェントが行動を選択（ε-greedy）
2. 次の状態に移動
3. すべての商品アイテムに対して：
   - 次の状態のQ値 > 前の状態のQ値 なら
   - Q(前の状態) ← Q(次の状態) × 0.9
4. 商品を発見したら、その位置のQ値を1000に設定
```

### 2.2 アルゴリズムの利点

1. **複数目標の効率的な探索**: ATM、複数の商品、レジを同時に探索
2. **価値の後方伝播**: 目標に近い状態から遠い状態へ価値を伝播
3. **並列学習**: 各目標の Q 値を独立して更新可能

### 2.3 アルゴリズムの課題

1. **理論的保証の欠如**: 標準的な Q 学習の収束保証が適用できない可能性
2. **更新条件の制約**: `Q(next) > Q(prev)` の条件により、更新が限定的
3. **報酬の統合**: 報酬（1000）が更新式に直接組み込まれていない

## 3. 実装の評価

### 3.1 良い点

1. **明確な構造**: モジュール化が適切

   - `Shopper`: エージェント
   - `Status`: 状態管理
   - `q_map_utils`: Q 学習ロジック

2. **柔軟な設定**: `config.json`でパラメータを調整可能

3. **可視化機能**: グラフ作成機能（`create_graphs.py`）

4. **画像認識の統合**: 商品判別に画像類似度を使用

### 3.2 改善の余地

1. **更新式の明確化**:

   - 現在の更新式の理論的根拠を文書化
   - 標準的な Q 学習との関係を説明

2. **報酬設計の改善**:

   - ステップごとの負の報酬（移動コスト）
   - より細かい報酬設計

3. **学習率の導入**:

   - 現在は固定値 0.9 を使用
   - 学習率パラメータの追加を検討

4. **収束性の検証**:
   - アルゴリズムの収束性を理論的・実験的に検証

## 4. 実験設計の評価

### 4.1 実験設定

- **ε-greedy**: `epsilon = 0.01`（探索率が非常に低い）
- **実行回数**: `runs_per_set = 100`, `sets = 4`
- **マップサイズ**: 20×50

### 4.2 評価指標

- ステップ数（`create_graphs.py`で可視化）
- 購入成功率（`is_shopping_successful`）

### 4.3 推奨される追加評価

1. **学習曲線の分析**: Q 値の変化を追跡
2. **探索率の影響**: 異なる ε 値での比較
3. **収束性の検証**: 十分なエピソード数での学習

## 5. 総合評価

### 5.1 学術的価値

- **独自性**: 並列 Q 更新法は興味深いアプローチ
- **実用性**: 複数目標の探索問題に適用可能
- **理論的発展の余地**: 標準的な Q 学習との関係を理論的に分析する価値がある

### 5.2 実装の完成度

- **コード品質**: 良好（モジュール化、可読性）
- **機能性**: 動作する実装
- **文書化**: 改善の余地あり（特にアルゴリズムの理論的背景）

### 5.3 推奨事項

1. **理論的背景の明確化**: なぜこの更新式が有効なのかを説明
2. **標準的な Q 学習との比較実験**: 同じ環境で標準的な Q 学習と性能比較
3. **ハイパーパラメータの系統的な探索**: ε、割引率、学習率など
4. **論文や参考文献の追加**: 類似手法との比較

## 6. 結論

このプロジェクトは**Q 学習に基づいた独自の強化学習アルゴリズム**として評価できます。標準的な Q 学習とは異なる更新式を使用していますが、Q 値テーブルと ε-greedy 方策を使用している点で、Q 学習の変形版として位置づけられます。

「並列 Q 更新法」という独自のアプローチは、複数目標の探索問題において興味深い特性を持っており、理論的な分析と実験的な検証の価値がある研究です。

---

## 7. 構造上の欠陥の分析

コードを詳細に分析した結果、以下の**重大な構造上の欠陥**が発見されました。

### 7.1 【重大】Q マップ更新のタイミングと座標の矛盾

**問題箇所：** `src/models/shopper.py` の `walk()` 関数

```56:108:src/models/shopper.py
    def walk(self, file):
        status = self.status

        next_direction = get_next_direction(status)
        next_x, next_y = get_next_x_y(status, next_direction)

        # 次の場所がマップの範囲外の時は何もしない
        if not (
            next_x >= 0
            and next_y >= 0
            and next_x < status.position.vertical
            and next_y < status.position.horizontal
        ):
            return

        next_items = []
        for n in range(3):
            next_items.append(status.store_map[n][next_x][next_y])

        # Qマップを更新
        update_all_q_map(status, next_direction)

        # 次の場所が通行可能なマスのとき
        if next_items[0] == " " or next_items[0] == "*":

            # マップを更新
            row = list(status.store_map[0][next_x])
            row[next_y] = "*"
            status.store_map[0][next_x] = "".join(row)

            # 位置情報更新
            status.position.move_to(next_x, next_y, next_direction)
```

**問題点：**

1. **更新タイミングの矛盾**
   - 76 行目で `update_all_q_map()` が呼ばれるが、この時点では**まだ位置が更新されていない**
   - 位置更新は 87 行目で行われる
   - しかし、`update_all_q_map()` 内では以下のように参照している：

```97:110:src/utils/q_map_utils.py
def update_all_q_map(status, next_direction):
    for i in range(len(status.shopping_list)):
        if (
            status.q_map[i][next_direction][status.position.x][status.position.y]
            > status.q_map[i][status.position.prev_d][status.position.prev_x][
                status.position.prev_y
            ]
        ):
            status.q_map[i][status.position.prev_d][status.position.prev_x][
                status.position.prev_y
            ] = (
                status.q_map[i][next_direction][status.position.x][status.position.y]
                * 0.9
            )
```

2. **座標参照の誤り**

   - `update_all_q_map()` は `status.position.x` と `status.position.y`（現在位置）を「次の位置」として使用している
   - しかし、実際の次の位置は `next_x`, `next_y` であり、まだ `status.position` には反映されていない
   - つまり、**前の位置の Q 値と現在位置の Q 値を比較している**が、本来は**現在位置と次の位置を比較すべき**

3. **意図された動作との不一致**
   - アルゴリズムの意図は「次の状態の Q 値 > 前の状態の Q 値」をチェックすること
   - しかし実装では「現在位置の Q 値 > 前の位置の Q 値」をチェックしている
   - これは論理的に矛盾している

**影響：**

- Q 値の更新が正しく機能しない可能性
- 学習が期待通りに進まない可能性
- アルゴリズムの意図と実装の不一致

**修正案：**

```python
# 位置更新後にQマップを更新する
status.position.move_to(next_x, next_y, next_direction)
update_all_q_map(status, next_direction)  # この時点でprev_x, prev_yが正しく設定されている
```

または、`update_all_q_map()` を修正して `next_x`, `next_y` を引数として受け取る。

### 7.2 商品発見時の位置更新について（設計上の判断）

**実装箇所：** `src/models/shopper.py` の `walk()` 関数

```100:108:src/models/shopper.py
        # 次の場所に商品がある時
        else:
            true_or_false, item_id = item_checker(status, next_items)
            if true_or_false:

                # マップと進捗を更新
                status.shopping_cart.update_progress()
                status.give_max_q_value(item_id, next_direction)
            return
```

**実装の意図：**

1. **商品の上には移動しない設計**

   - 商品を発見した場合、エージェントは商品の位置（`next_x`, `next_y`）には移動しない
   - これは意図的な設計であり、商品の上に乗らないようにするため

2. **Q 値の更新方法**
   - `give_max_q_value()` は現在位置（`status.position.x`, `status.position.y`）から、商品の方向（`next_direction`）の Q 値を 1000 に設定：

```17:18:src/utils/status.py
    def give_max_q_value(self, item_id, direction):
        self.q_map[item_id][direction][self.position.x][self.position.y] = 1000
```

- これは「この位置からこの方向に進むと商品が見つかる」という情報を記録する設計
- 実装は意図通りに動作している

**評価：**

- ✅ 設計として合理的：商品の上に移動しない
- ✅ 実装は意図通り：現在位置から商品方向の Q 値を更新
- ✅ 問題なし：この実装は正しく機能している

**注意点：**

この設計では、商品を発見した時点での位置から商品方向の Q 値が更新されるため、同じ位置から異なる方向に商品がある場合、最後に見つけた方向の Q 値のみが 1000 に設定される。これは設計上の判断として受け入れられる。

### 7.3 【中程度】範囲外移動時の Q マップ更新の欠如

**問題箇所：** `src/models/shopper.py` の `walk()` 関数

```62:69:src/models/shopper.py
        # 次の場所がマップの範囲外の時は何もしない
        if not (
            next_x >= 0
            and next_y >= 0
            and next_x < status.position.vertical
            and next_y < status.position.horizontal
        ):
            return
```

**問題点：**

- 範囲外への移動が試みられた場合、`return` で処理が終了する
- この場合、Q マップの更新が行われない
- しかし、範囲外への移動を試みたという情報は学習に有用な可能性がある

**影響：**

- 範囲外への移動を避ける学習ができない
- エージェントが同じ範囲外への移動を繰り返す可能性

**修正案：**
範囲外への移動に対して負の報酬を設定するか、Q 値を更新する仕組みを追加。

### 7.4 【中程度】初期状態での prev_x, prev_y の設定

**問題箇所：** `src/utils/status.py` の `Position` クラス

```22:32:src/utils/status.py
class Position:
    def __init__(self, x, y, vertical, horizontal):
        self.x = x
        self.y = y
        self.d = 0
        self.steps = 0
        self.prev_x = x
        self.prev_y = y
        self.prev_d = 0
        self.vertical = vertical
        self.horizontal = horizontal
```

**問題点：**

- 初期化時、`prev_x = x`, `prev_y = y` となっている
- 最初の移動時、`prev_x` と `prev_y` は現在位置と同じ値になる
- `update_all_q_map()` で `Q(prev) < Q(next)` の比較が行われるが、最初の更新時は `prev_x == x`, `prev_y == y` の可能性がある

**影響：**

- 最初の更新時に予期しない動作をする可能性
- ただし、最初の移動後は `move_to()` で正しく更新されるため、大きな問題にはならない

**修正案：**
初期状態では `prev_x`, `prev_y` を `None` または `-1` に設定し、最初の更新時はスキップする。

### 7.5 【軽微】無限ループの可能性

**問題箇所：** `src/main.py` のメインループ

```60:63:src/main.py
    # 8, 歩く(メインループ)
    with open(output_file_path, "a") as file:
        while status.shopping_cart.progress < status.shopping_cart.item_amount:
            shopper.walk(file)
```

**問題点：**

- `walk()` 関数が何も更新しない場合（範囲外への移動、スタート地点への移動など）、`progress` が増加しない
- エージェントが同じ位置にとどまり続ける可能性がある
- 無限ループに陥る可能性

**影響：**

- プログラムが終了しない
- ただし、ε-greedy 方策によりランダムに移動するため、実際には無限ループになる可能性は低い

**修正案：**
最大ステップ数の制限を追加：

```python
max_steps = 10000
step_count = 0
while status.shopping_cart.progress < status.shopping_cart.item_amount and step_count < max_steps:
    shopper.walk(file)
    step_count += 1
```

### 7.6 【軽微】状態更新の順序の問題

**問題箇所：** `src/models/shopper.py` の `walk()` 関数全体

**問題点：**

現在の更新順序：

1. Q マップ更新（76 行目）← 位置更新前
2. 位置更新（87 行目）← 位置更新後

しかし、Q マップ更新は位置情報に依存しているため、**位置更新後に実行すべき**。

**影響：**

- 上記の 7.1 の問題と関連
- 状態の不整合

### 7.7 【軽微】商品発見時のマップ更新の欠如

**問題箇所：** `src/models/shopper.py` の `walk()` 関数

```100:108:src/models/shopper.py
        # 次の場所に商品がある時
        else:
            true_or_false, item_id = item_checker(status, next_items)
            if true_or_false:

                # マップと進捗を更新
                status.shopping_cart.update_progress()
                status.give_max_q_value(item_id, next_direction)
            return
```

**問題点：**

- 商品を発見した場合、`store_map` が更新されない（通行可能なマスの場合は更新される：82-84 行目）
- 一貫性がない

**影響：**

- マップの表示が一貫しない
- デバッグが困難

## 8. 構造上の欠陥の総括

### 8.1 重大度別の分類

| 重大度     | 問題                                 | 影響                                 |
| ---------- | ------------------------------------ | ------------------------------------ |
| **重大**   | Q マップ更新のタイミングと座標の矛盾 | アルゴリズムが正しく機能しない可能性 |
| **中程度** | 範囲外移動時の Q マップ更新の欠如    | 学習が不完全                         |
| **中程度** | 初期状態での prev_x, prev_y の設定   | 最初の更新時の予期しない動作         |
| **軽微**   | 無限ループの可能性                   | プログラムが終了しない可能性         |
| **軽微**   | 状態更新の順序の問題                 | 状態の不整合                         |
| **軽微**   | 商品発見時のマップ更新の欠如         | 一貫性の欠如                         |

**注：** 7.2（商品発見時の位置更新）は設計上の判断として問題なしと判断。商品の上には移動しない設計であり、現在位置から商品方向の Q 値を更新する実装は意図通りに動作している。

### 8.2 推奨される修正の優先順位

1. **最優先**: Q マップ更新のタイミングと座標の修正（7.1）
2. **中優先**: 範囲外移動時の処理の改善（7.3）
3. **低優先**: その他の軽微な問題（7.4-7.7）

**注：** 7.2（商品発見時の位置更新）は設計上の判断として問題なしと判断したため、修正不要。

### 8.3 修正後の期待される効果

- アルゴリズムが意図通りに動作する
- 学習が正しく進行する
- 報酬が正しい位置に設定される
- コードの一貫性が向上する
