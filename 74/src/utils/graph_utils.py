import matplotlib.pyplot as plt
import re
import os
from config_utils import *


def create_list_of_steps(data_dir):
    steps = []

    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    match = re.search(r"Steps: (\d+)", line)
                    if match:
                        steps.append(int(match.group(1)))
                        break
    return steps


def create_graph(steps, graph_title, file_name):
    plt.plot(steps, marker="o", linestyle="-")
    plt.xlabel("Number of attempts", fontsize=18)
    plt.ylabel("Steps", fontsize=20)
    plt.title(f"{graph_title}", fontsize=20, y=1.1)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid(True)
    plt.tight_layout(pad=2.0)
    plt.savefig(file_name, dpi=600)
    plt.close()


# 設定ファイルを読み込む
version = get_project_version()
runs_per_set = get_runs_per_set()
sets = get_sets()
title = get_title()

root_dir = get_root_dir()

for num_of_set in range(sets):
    data_dir = os.path.join(root_dir, f"output/data/{num_of_set}")
    steps = create_list_of_steps(data_dir)

    file_name = os.path.join(
        root_dir, f"output/graphs/{version}_graph_{num_of_set}.png"
    )
    create_graph(steps, version, file_name)
