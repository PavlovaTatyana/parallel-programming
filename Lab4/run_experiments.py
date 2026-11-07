import subprocess
import re
import csv

N_VALUES = [200, 400, 800, 1200, 1600, 2000]
BLOCK_SIZES = [8, 16, 32] 

results = []

print(f"{'N':>6} {'Block':>6} {'Time (s)':>12}")
print("-" * 30)

for n in N_VALUES:
    for b in BLOCK_SIZES:
        result = subprocess.run(["./lab4", str(n), str(b)], capture_output=True, text=True)
        
        match = re.search(r"Time=([\d.eE+-]+)", result.stdout)
        if match:
            t = float(match.group(1))
            results.append({"N": n, "Block": b, "Time": t})
            print(f"{n:>6} {b:>6} {t:>12.5f}")

with open("times.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["N", "Block", "Time"])
    writer.writeheader()
    writer.writerows(results)

print("\nСохранено в times.csv")