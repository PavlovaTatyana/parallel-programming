import subprocess
import re
import csv
import os

N_VALUES = [200, 400, 800, 1200, 1600] 
THREADS = [1, 2, 4, 8]

EXE = "result.exe" if os.name == 'nt' else "./result"

results = []

print(f"{'N':>6} | {'Потоки':>6} | {'Время (сек)':>12}")
print("-" * 30)

for n in N_VALUES:
    time_1_thread = None
    
    for t in THREADS:
        
        process = subprocess.run([EXE, str(n), str(t)], capture_output=True, text=True)
        
        match = re.search(r"Время выполнения:\s*([\d.eE+-]+)", process.stdout)
        if match:
            current_time = float(match.group(1))
            print(f"{n:>6} | {t:>6} | {current_time:>12.4f}")
            
            if t == 1:
                time_1_thread = current_time
                
            if time_1_thread:
                speedup = time_1_thread / current_time
                efficiency = (speedup / t) * 100
            else:
                speedup = 1.0
                efficiency = 100.0
                
            results.append([n, t, current_time, speedup, efficiency])
        else:
            print(f"Ошибка парсинга для N={n}, потоков={t}")
            print(process.stdout)
            

with open("times.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["N", "Потоки", "Время (сек)", "Ускорение", "Эффективность"])
    writer.writerows(results)

print("\nДанные сохранены в times.csv")