import csv
import numpy as np
import matplotlib.pyplot as plt


def load_csv(path="times.csv"):
    N, t_avg, ops = [], [], []
    with open(path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            N.append(int(row["N"]))
            t_avg.append(float(row["time_avg"]))
            ops.append(int(row["operations"]))
    return np.array(N), np.array(t_avg), np.array(ops)


def main():
    N, t_avg, ops = load_csv()

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(N, t_avg, "o-", color="tab:blue",
            label="Эксперимент (среднее из 3 запусков)")

    k = t_avg[-1] / (N[-1] ** 3)
    N_dense = np.linspace(N.min(), N.max(), 300)
    ax.plot(N_dense, k * N_dense ** 3, "--", color="tab:red",
            label=r"Теория: $O(N^3)$")

    ax.set_xlabel("Размер матрицы N")
    ax.set_ylabel("Среднее время умножения, с")
    ax.set_title("Зависимость времени умножения матриц от размера N")
    ax.grid(True, ls=":", alpha=0.6)
    ax.legend()

    fig.tight_layout()
    fig.savefig("time_vs_N.png", dpi=150)
    print("Сохранено: time_vs_N.png")

    log_N = np.log(N)
    log_t = np.log(t_avg)
    p, log_k = np.polyfit(log_N, log_t, 1)

    print(f"\nОценка показателя степени из данных: p ≈ {p:.3f}")
    print("  Теоретически для O(N^3) ожидается p ≈ 3.0")
    if 2.7 <= p <= 3.3:
        print("  Результат согласуется с O(N^3) ✅")
    else:
        print("  Отклонение от O(N^3) — возможно, влияет кэш, I/O, шум ОС")

    print("\nТаблица результатов:")
    print(f"{'N':>6} {'t_avg, с':>12} {'N^3':>14} {'t / N^3, нс':>14}")
    for n, t in zip(N, t_avg):
        print(f"{n:>6} {t:>12.6f} {n**3:>14} {t / (n**3) * 1e9:>14.4f}")


if __name__ == "__main__":
    main()