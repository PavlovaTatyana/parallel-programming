import subprocess
import re
import csv
import sys
import os

N_VALUES = [200, 400, 800, 1200, 1600, 2000]
REPEATS = 3

EXE = "result.exe"
CSV_OUT = "times.csv"


def run_once(n):
    try:
        result = subprocess.run(
            [EXE],
            input=f"{n}\n",
            capture_output=True,
            text=True,
            timeout=600,
        )
    except subprocess.TimeoutExpired:
        print(f"  Таймаут при N={n}")
        return None, None

    m_time = re.search(r"Время выполнения:\s*([\d.eE+-]+)", result.stdout)
    m_ops = re.search(r"Объём задачи:\s*(\d+)", result.stdout)

    if not m_time or not m_ops:
        print(f"  Не удалось распарсить вывод для N={n}")
        print(result.stdout)
        print(result.stderr)
        return None, None

    return float(m_time.group(1)), int(m_ops.group(1))


def main():
    if not os.path.exists(EXE):
        print(f"ОШИБКА: {EXE} не найден. Сначала соберите C++ программу.")
        sys.exit(1)

    rows = []
    print(f"{'N':>6} {'запуск':>8} {'время, сек':>14} {'операций':>14}")
    print("-" * 50)

    for n in N_VALUES:
        times = []
        ops = None
        for rep in range(1, REPEATS + 1):
            t, o = run_once(n)
            if t is None:
                print(f"{n:>6} {rep:>8}  ошибка")
                continue
            times.append(t)
            ops = o
            print(f"{n:>6} {rep:>8} {t:>14.6f} {ops:>14}")

        if times:
            t_avg = sum(times) / len(times)
            rows.append({
                "N": n,
                "time_avg": t_avg,
                "operations": ops,
            })
            print(f"{n:>6} {'СРЕДНЕЕ':>8} {t_avg:>14.6f} {ops:>14}")
            print("-" * 50)
        else:
            print(f"{n:>6}  не удалось выполнить ни одного запуска")
            print("-" * 50)

    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["N", "time_avg", "operations"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nДанные сохранены в {CSV_OUT}")
    print(f"Всего точек: {len(rows)}")


if __name__ == "__main__":
    main()