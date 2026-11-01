# verify.py
import numpy as np
import sys
import os

def read_matrix(path, skip_trailing_lines=0):
    """
    Читает матрицу из текстового файла.
    Первая строка — размер N.
    Далее N строк по N чисел.
    Если skip_trailing_lines > 0 — пропускает указанное число строк в конце (для result.txt).
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Первая строка — размер
    N = int(lines[0].strip())

    # Следующие N строк — матрица
    rows = []
    for i in range(1, N + 1):
        row = list(map(float, lines[i].split()))
        if len(row) != N:
            raise ValueError(f"В строке {i + 1} файла {path} {len(row)} чисел, ожидалось {N}")
        rows.append(row)

    return np.array(rows, dtype=np.float64), N


def main():
    # Пути к файлам (в текущей папке)
    fileA = "matrixA.txt"
    fileB = "matrixB.txt"
    fileR = "result.txt"

    # Проверяем, что все файлы есть
    for f in (fileA, fileB, fileR):
        if not os.path.exists(f):
            print(f"ОШИБКА: файл {f} не найден. Запустите C++ программу сначала.")
            sys.exit(1)

    # --- 1. Читаем исходные данные и результат C++ ---
    A, N_A = read_matrix(fileA)
    B, N_B = read_matrix(fileB)
    C_cpp, N_C = read_matrix(fileR)

    print("=" * 60)
    print("ВЕРИФИКАЦИЯ РЕЗУЛЬТАТА УМНОЖЕНИЯ МАТРИЦ")
    print("=" * 60)
    print(f"Размеры: A = {A.shape}, B = {B.shape}, C = {C_cpp.shape}")

    # Проверка согласованности размеров
    if not (N_A == N_B == N_C):
        print(f"ОШИБКА: размеры не совпадают: A={N_A}, B={N_B}, C={N_C}")
        sys.exit(1)

    # --- 2. Независимое вычисление через NumPy ---
    C_np = A @ B   # оператор @ в NumPy — это матричное умножение (BLAS)

    # --- 3. Сравнение ---
    # Абсолютная разница поэлементно
    abs_diff = np.abs(C_cpp - C_np)

    # Максимальная абсолютная погрешность
    max_abs_err = abs_diff.max()

    # Относительная погрешность (по отношению к элементам C_np)
    # Защита от деления на ноль: там, где |C_np| мало, берём 1 как знаменатель
    denom = np.where(np.abs(C_np) > 1e-12, np.abs(C_np), 1.0)
    max_rel_err = (abs_diff / denom).max()

    scale = max(np.abs(A).max(), np.abs(B).max(), np.abs(C_np).max())
    eps = np.finfo(np.float64).eps
    expected_tol = eps * N_A * scale * 10
    # --- 4. Вывод ---
    print("-" * 60)
    print(f"N                       : {N_A}")
    print(f"Максимальный элемент |A|: {np.abs(A).max():.6e}")
    print(f"Максимальный элемент |B|: {np.abs(B).max():.6e}")
    print(f"Максимальный элемент |C|: {np.abs(C_np).max():.6e}")
    print("-" * 60)
    print(f"Макс. абсолютная погрешность : {max_abs_err:.6e}")
    print(f"Макс. относительная погрешность: {max_rel_err:.6e}")
    print(f"Ожидаемый порядок (машинный):  ~ {expected_tol:.6e}")
    print("-" * 60)

    if max_abs_err <= expected_tol:
        print("РЕЗУЛЬТАТ: ВЕРИФИКАЦИЯ ПРОЙДЕНА ✅")
        print("C++ и NumPy дают согласованный результат в пределах машинной точности.")
        return 0
    else:
        print("РЕЗУЛЬТАТ: ВЕРИФИКАЦИЯ НЕ ПРОЙДЕНА ❌")
        print("Разница превышает ожидаемую машинную точность.")
        print("Возможные причины:")
        print("  - ошибка в C++ коде,")
        print("  - несовпадение N между файлами,")
        print("  - повреждённые/устаревшие файлы.")
        # Покажем топ-5 крупнейших расхождений
        idx = np.unravel_index(np.argsort(-abs_diff, axis=None)[:5], abs_diff.shape)
        print("\nТоп-5 крупнейших расхождений:")
        for i, j in zip(*idx):
            print(f"  C[{i}][{j}]: C++ = {C_cpp[i, j]:.15e}, "
                  f"NumPy = {C_np[i, j]:.15e}, Δ = {abs_diff[i, j]:.3e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())