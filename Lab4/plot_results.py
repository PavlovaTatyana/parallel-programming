import csv
import matplotlib.pyplot as plt

data = {}
with open("times.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n = int(row["N"])
        b = int(row["Block"])
        t = float(row["Time"])
        
        if b not in data:
            data[b] = {"N": [], "Time": []}
        data[b]["N"].append(n)
        data[b]["Time"].append(t)

plt.figure(figsize=(10, 6))

for b, vals in data.items():
    plt.plot(vals["N"], vals["Time"], marker='o', label=f'Блок {b}x{b}')

plt.xlabel("Размер матрицы N")
plt.ylabel("Время выполнения (сек)")
plt.title("Зависимость времени умножения от N и размера блока (CUDA)")
plt.grid(True, linestyle='--')
plt.legend()

plt.savefig("lab4_plot.png", dpi=150)
plt.close()

print("График успешно сохранен в lab4_plot.png")