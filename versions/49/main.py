import matplotlib.pyplot as plt
import re
import os


title = "Sequential Q update method"
# title = "Sequential and Parallel Q update method"
# title = "Parallel Q update method"

def create_graph(directory, name):
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

    output_file = "stats.txt"
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"Title: {name}\n")
        f.write(f"Min: {min_steps}\n")
        f.write(f"Max: {max_steps}\n")
        f.write(f"Average: {average_steps:.2f}\n")
        f.write("\n")

    # From 1 to 1000
    plt.plot(steps, marker="o", linestyle="-")
    plt.xlabel("Number of attempts", fontsize=18)
    plt.ylabel("Steps", fontsize=20)
    plt.title(f"{title}", fontsize=20, y=1.1)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid(True)
    plt.tight_layout(pad=2.0)
    plt.savefig(f"./graph/{name}_graph_1_1000.png", dpi=600)
    plt.close()

    # from 900 to 1000
    steps_subset = steps[900:1000]
    plt.plot(range(900, 1000), steps_subset, marker="o", linestyle="-")
    plt.xlabel("Number of attempts (900 to 1000)", fontsize=20)
    plt.ylabel("Steps", fontsize=20)
    plt.title(f"{title}\nSteps from 900 to 1000", fontsize=18, y=1.1)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.ylim(50, 1000)
    plt.grid(True)
    plt.tight_layout(pad=2.0)
    plt.savefig(f"./graph/{name}_graph_900_1000.png", dpi=600)
    plt.close()


for d in range(3):
    directory = f"./data/map{d}"

    file_path = os.path.join(directory, f"e20")
    name = f"df49_map{d}_e20"
    create_graph(file_path, name)

    file_path = os.path.join(directory, f"e50")
    name = f"df49_map{d}_e50"
    create_graph(file_path, name)

    file_path = os.path.join(directory, f"e80")
    name = f"df49_map{d}_e80"
    create_graph(file_path, name)