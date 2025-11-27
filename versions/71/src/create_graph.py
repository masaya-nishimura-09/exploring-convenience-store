import matplotlib.pyplot as plt
import os
from io_utils import get_root_dir
import pandas as pd


def create_graph():
    root_dir = get_root_dir()

    for csv_file in os.listdir(root_dir + "/output/stats"):
        csv_file_path = os.path.join(root_dir, "output/stats", csv_file)
        # CSVを読み込む
        df = pd.read_csv(csv_file_path)

        # グラフのサイズを調整
        plt.figure(figsize=(10, 8))

        # 棒グラフを作成
        plt.bar(df["Name2"], df["Similarity"])

        # タイトルと軸ラベル
        plt.title(f"Similarity Comparison for {df['Name1'][0]}", fontsize=20)
        plt.xlabel("Items", fontsize=16)
        plt.ylabel("Similarity", fontsize=16)

        # x軸のラベルを少し回転
        plt.xticks(rotation=60, fontsize=9)
        plt.yticks(fontsize=9)

        # グリッドを表示（任意）
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout(pad=2.0)

        # グラフを保存
        file_name = os.path.join(
            root_dir, "output/graphs", f"{df['Name1'][0]}_similarity_graph.png"
        )
        plt.savefig(file_name, dpi=600)
