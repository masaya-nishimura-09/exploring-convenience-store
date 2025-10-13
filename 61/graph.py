import matplotlib.pyplot as plt
import re
import os
import csv

DF_FILE = 61

# TITLE = "Sequential Q update method"
# TITLE = "Sequential and Parallel Q update method"
TITLE = "Parallel Q update method"

def create_graph(x, y, ylabel, filename):
    plt.plot(x, y, marker="o", linestyle="-")
    plt.xlabel("Epsilons(%)", fontsize=18)
    plt.ylabel(ylabel, fontsize=20)
    plt.title(f"{TITLE}", fontsize=20, y=1.1)
    plt.xticks(x, fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid(True)
    plt.tight_layout(pad=2)
    plt.savefig(filename, dpi=600)
    plt.close()

def output_data(directory, name, csv_writer, map_number):
    min_steps = 0
    max_steps = 0
    average_steps = 0
    steps = []
    steps0 = []
    steps1 = []
    steps2 = []
    steps3 = []

    for num in range(0, 4):

        current_directory = os.path.join(directory, f"{num}")

        for filename in sorted(os.listdir(current_directory)):
            if filename.endswith(".txt"):
                file_path = os.path.join(current_directory, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    for line in file:
                        match = re.search(r"Steps: (\d+)", line)
                        if match:
                            if num == 0:
                                steps0.append(int(match.group(1)))
                            elif num == 1:
                                steps1.append(int(match.group(1)))
                            elif num == 2:
                                steps2.append(int(match.group(1)))
                            elif num == 3:
                                steps3.append(int(match.group(1)))
                            break

        if num == 0:
            min_steps = min_steps + min(steps0)
            max_steps = max_steps + max(steps0)
            average_steps = average_steps + sum(steps0) / len(steps0) if steps0 else 0
        elif num == 1:
            min_steps = min_steps + min(steps1)
            max_steps = max_steps + max(steps1)
            average_steps = average_steps + sum(steps1) / len(steps1) if steps1 else 0
        elif num == 2:
            min_steps = min_steps + min(steps2)
            max_steps = max_steps + max(steps2)
            average_steps = average_steps + sum(steps2) / len(steps2) if steps2 else 0
        elif num == 3:
            min_steps = min_steps + min(steps3)
            max_steps = max_steps + max(steps3)
            average_steps = average_steps + sum(steps3) / len(steps3) if steps3 else 0

    for n in range(0, 1000):
        total = steps0[n] + steps1[n] + steps2[n] + steps3[n]
        ave = total / 4
        steps.append(ave)


    min_steps = min_steps / 4
    max_steps = max_steps / 4
    average_steps = average_steps / 4

    csv_writer.writerow([name, map_number, min_steps, max_steps, f"{average_steps:.2f}"])

with open('stats.csv', 'w', newline='', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['Title', 'Map', 'Min', 'Max', 'Average'])

    for d in range(3):
        directory = f"./data/map{d}"
        name = f"file{DF_FILE}_map{d}_e1percent"
        output_data(directory, name, csv_writer, d)

epsilons = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

map0_titles = []
map1_titles = []
map2_titles = []

map0_mins = []
map1_mins = []
map2_mins = []

map0_maxs = []
map1_maxs = []
map2_maxs = []

map0_averages = []
map1_averages = []
map2_averages = []