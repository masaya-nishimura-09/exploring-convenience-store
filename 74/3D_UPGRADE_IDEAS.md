# 3 次元マップ化の改良アイデア

## 概要

現在の 2 次元マップ（x, y 座標）を 3 次元マップ（x, y, z 座標）に拡張し、棚の高さを 3 層にする。

## 主な変更点

### 1. データ構造の変更

#### 現在の構造

- `map_data`: 文字列の配列（2D）
- `Position`: x, y 座標のみ

#### 3D 化後の構造

- `map_data`: 3 次元配列（リストのリストのリスト）または辞書形式
  ```python
  map_data = {
      0: [  # z=0 (床レベル)
          "--        TDHEFVTGADQRIFIGKJABGQICLQQDHFQ         ",
          ...
      ],
      1: [  # z=1 (中段)
          "--        TDHEFVTGADQRIFIGKJABGQICLQQDHFQ         ",
          ...
      ],
      2: [  # z=2 (上段)
          "--        TDHEFVTGADQRIFIGKJABGQICLQQDHFQ         ",
          ...
      ]
  }
  ```
  または
  ```python
  map_data = [
      [  # z=0
          "--        TDHEFVTGADQRIFIGKJABGQICLQQDHFQ         ",
          ...
      ],
      [  # z=1
          ...
      ],
      [  # z=2
          ...
      ]
  ]
  ```

### 2. Position クラスの拡張

```python
class Position:
    def __init__(self, x, y, z, vertical, horizontal, depth):
        self.x = x
        self.y = y
        self.z = z  # 新規追加（0, 1, 2の3層）
        self.d = 0
        self.steps = 0
        self.prev_x = x
        self.prev_y = y
        self.prev_z = z  # 新規追加
        self.prev_d = 0
        self.vertical = vertical
        self.horizontal = horizontal
        self.depth = depth  # 新規追加（通常は3）

    def move_to(self, x, y, z, d):
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_z = self.z
        self.x = x
        self.y = y
        self.z = z
        self.prev_d = d
        self.steps += 1
```

### 3. 移動方向の拡張

#### 現在の移動方向（8 方向）

- 0: 上 (-1, 0)
- 1: 右上 (-1, +1)
- 2: 右 (0, +1)
- 3: 右下 (+1, +1)
- 4: 下 (+1, 0)
- 5: 左下 (+1, -1)
- 6: 左 (0, -1)
- 7: 左上 (-1, -1)

#### 3D 化後の移動方向（10 方向または 26 方向）

**オプション 1: 10 方向（実用的）**

- 0-7: 現在の 8 方向（同じ z レベル）
- 8: 上に移動（z+1、階段/エレベーター経由）
- 9: 下に移動（z-1、階段/エレベーター経由）

**オプション 2: 26 方向（完全 3D）**

- 8 方向 × 3 層 = 24 方向 + 上下移動 2 方向 = 26 方向

### 4. Q マップの 3D 化

```python
# 現在: q_map[item_id][direction][x][y]
# 3D化後: q_map[item_id][direction][x][y][z]

def get_q_map(item_amount: int, vertical: int, depth: int) -> list:
    q_map = []
    for i in range(item_amount):
        item_q = []
        for j in range(10):  # 10方向（8方向 + 上下）
            current_q = []
            for z in range(depth):  # z軸を追加
                # qファイルの読み込み（z層ごとにファイルを分けるか、1ファイルに全層を含める）
                ...
            item_q.append(current_q)
        q_map.append(item_q)
    return q_map
```

### 5. マップアクセスの変更

```python
# 現在
next_tile = status.store_map[next_x][next_y]

# 3D化後
next_tile = status.store_map[next_z][next_x][next_y]
```

### 6. 表示方法の改善

#### オプション 1: 複数レイヤーを並べて表示

```
Map (Floor 0):
--        TDHEFVTGADQRIFIGKJABGQICLQQDHFQ
...

Map (Floor 1):
--        TDHEFVTGADQRIFIGKJABGQICLQQDHFQ
...

Map (Floor 2):
--        TDHEFVTGADQRIFIGKJABGQICLQQDHFQ
...

Current Position: (x=19, y=4, z=1)
```

#### オプション 2: 現在の階層のみ表示

```
Current Floor: 1
Map:
--        TDHEFVTGADQRIFIGKJABGQICLQQDHFQ
...

Position: (x=19, y=4, z=1)
```

#### オプション 3: 3D 可視化（将来的に）

- Matplotlib や VTK を使用した 3D 可視化
- Web ベースの 3D 可視化（Three.js など）

### 7. 階段/エレベーターの実装

3D マップでは階層間の移動が必要：

- 特定の位置（例: マップ上の特定の記号）で上下移動可能
- 例: `"S"` = 階段（Stairs）、`"E"` = エレベーター（Elevator）

```python
# 階段の位置を定義
stairs_positions = [
    (5, 10, 0),  # 1階の階段
    (5, 10, 1),  # 2階の階段
    (5, 10, 2),  # 3階の階段
]

# 階段の位置にいる場合のみ上下移動可能
if (next_x, next_y, next_z) in stairs_positions:
    # 上下移動を許可
```

### 8. 商品配置の 3D 化

商品を異なる階層に配置可能に：

- 同じ商品が複数の階層に存在可能
- 階層ごとに異なる商品を配置可能

```python
# 商品マッピングの拡張
# 現在: 文字 → 商品
# 3D化後: (文字, z) → 商品 または 文字 → 商品（階層に関係なく）
```

### 9. 実装の優先順位

1. **Phase 1: 基本構造の変更**

   - Position クラスに z 座標を追加
   - map_data を 3 次元配列に変更
   - 基本的な 3 層マップの読み込み

2. **Phase 2: 移動ロジックの拡張**

   - get_next_x_y → get_next_x_y_z に変更
   - 上下移動の実装（10 方向）

3. **Phase 3: Q マップの 3D 化**

   - Q マップファイル構造の変更
   - Q 値の更新ロジックを 3D 対応

4. **Phase 4: 表示の改善**

   - 3D マップの表示方法の実装
   - 現在位置の表示に z 座標を追加

5. **Phase 5: 階段/エレベーターの実装**
   - 階層間移動の制約を追加

## 技術的な考慮事項

### メモリ使用量

- 3D 化により Q マップのサイズが depth 倍に増加
- 例: 20×50×3 = 3000 セル（2D では 1000 セル）

### パフォーマンス

- Q 値の更新処理が増加
- 探索空間が拡大（学習に時間がかかる可能性）

### 後方互換性

- 既存の 2D マップデータとの互換性を保つか、変換スクリプトを作成

## 実装例のスニペット

### マップデータの読み込み

```python
def load_3d_map(map_data_2d, depth=3):
    """2Dマップを3Dマップに変換（各階層は同じマップ）"""
    map_3d = []
    for z in range(depth):
        map_3d.append([row[:] for row in map_data_2d])  # コピー
    return map_3d
```

### 移動方向の計算

```python
def get_next_x_y_z(status, direction):
    next_x = status.position.x
    next_y = status.position.y
    next_z = status.position.z

    # 水平方向の移動（0-7）
    if direction < 8:
        # 既存の8方向のロジック
        ...
    # 上に移動（8）
    elif direction == 8:
        next_z = min(status.position.z + 1, status.position.depth - 1)
    # 下に移動（9）
    elif direction == 9:
        next_z = max(status.position.z - 1, 0)

    return next_x, next_y, next_z
```

## まとめ

3 次元化により、より現実的なコンビニエンスストアの探索が可能になります。特に棚の高さを考慮した商品配置や、階層間の移動が可能になります。段階的な実装により、既存の機能を保ちながら拡張できます。
