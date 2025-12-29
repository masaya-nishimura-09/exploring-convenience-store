import matplotlib.pyplot as plt
import re
import os

directory = "./output"

title = "Sequential Q update method"
# title = "Sequential and Parallel Q update method"
# title = "Parallel Q update method"

steps = []

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                match = re.search(r"Steps: (\d+)", line)
                if match:
                    steps.append(int(match.group(1)))
                    break

# Min
min_steps = min(steps)
print("Min:", min_steps)

# Max
max_steps = max(steps)
print("Max:", max_steps)

# Average (Mean)
average_steps = sum(steps) / len(steps) if steps else 0
print("Average:", average_steps)

# From 1 to 1000
plt.plot(steps, marker="o", linestyle="-")
plt.xlabel("Number of attempts", fontsize=20)
plt.ylabel("Steps", fontsize=20)
plt.title(f"{title}", fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.grid(True)
plt.show()

# from 900 to 1000
steps_subset = steps[900:1000]
plt.plot(range(900, 1000), steps_subset, marker="o", linestyle="-")
plt.xlabel("Number of attempts (900 to 1000)", fontsize=20)
plt.ylabel("Steps", fontsize=20)
plt.title(f"{title}: Steps from 900 to 1000", fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylim(65, 200)
plt.grid(True)
plt.show()