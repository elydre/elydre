import os

path = os.path.dirname(os.path.abspath(__file__))

with open(f"{path}/include/kernel/system.h", "r") as f:
    for line in f:
        if "KERNEL_VERSION" not in line: continue
        print(line.split(" ")[-1][1:-2])
        break
