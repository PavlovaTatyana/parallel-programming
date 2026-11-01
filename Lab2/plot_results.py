import csv
import matplotlib.pyplot as plt

data = {}
with open("times.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n = int(row["N"])
        t = int(row["Потоки"])
        time_val = float(row["Время (сек)"])
        speedup = float(row["Ускорение"])
        efficiency = float(row["Эффективность"])
        
        if n not in data:
            data[n] = {"threads": [], "time": [], "speedup": [], "efficiency": []}
        
        data[n]["threads"].append(t)
        data[n]["time"].append(time_val)
        data[n]["speedup"].append(speedup)
        data[n]["efficiency"].append(efficiency)

Ns = sorted(list(data.keys()))
max_threads = max([max(v["threads"]) for v in data.values()])

plt.figure(figsize=(9, 6))
for n in Ns:
    vals = data[n]
    plt.plot(vals["threads"], vals["speedup"], marker='o', label=f'N={n}')

plt.plot([1, max_threads], [1, max_threads], 'k--', label='Идеальное ускорение y=x')

plt.xlabel("Количество потоков")
plt.ylabel("Ускорение (Speedup)")
plt.title("Зависимость ускорения от количества потоков")
plt.xticks([1, 2, 4, 8, 12, 16]) 
plt.grid(True, linestyle=':')
plt.legend()
plt.savefig("speedup.png", dpi=150, bbox_inches='tight')
plt.close()

plt.figure(figsize=(9, 6))

time_1 = [data[n]["time"][data[n]["threads"].index(1)] for n in Ns]
time_max = [data[n]["time"][data[n]["threads"].index(max_threads)] for n in Ns]

plt.plot(Ns, time_1, marker='s', label='1 поток (последовательно)')
plt.plot(Ns, time_max, marker='o', label=f'{max_threads} потоков (OpenMP)')

plt.xlabel("Размер матрицы N")
plt.ylabel("Время (сек)")
plt.title("Сравнение времени выполнения (1 поток vs OpenMP)")
plt.grid(True, linestyle=':')
plt.legend()
plt.savefig("time_comparison.png", dpi=150, bbox_inches='tight')
plt.close()

md_lines = []
md_lines.append("| N | Потоки | Время (сек) | Ускорение | Эффективность |")
md_lines.append("|---:|---:|---:|---:|---:|")

for n in Ns:
    for i in range(len(data[n]["threads"])):
        t = data[n]["threads"][i]
        time_val = data[n]["time"][i]
        speedup = data[n]["speedup"][i]
        eff = data[n]["efficiency"][i]
        
        md_lines.append(f"| {n} | {t} | {time_val:.4f} | {speedup:.2f} | {eff:.1f}% |")

with open("table.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print("Сохранены файлы:")
print("1. speedup.png (график ускорения)")
print("2. time_comparison.png (график времени)")
print("3. table.md (готовая таблица для README.md)")