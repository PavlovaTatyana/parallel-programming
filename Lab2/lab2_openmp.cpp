#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <cstdlib>
#include <ctime>
#include <string>
#include <stdexcept>
#include <omp.h> 

using Matrix = std::vector<double>;

const int FILE_WRITE_LIMIT = 200;

void generateAndWrite(const std::string& filename, int N, Matrix& M) {
    std::srand(std::time(nullptr) + std::rand());
    for (int i = 0; i < N * N; ++i)
        M[i] = (double)std::rand() / RAND_MAX;

    std::ofstream f(filename, std::ios::trunc);
    if (!f.is_open())
        throw std::runtime_error("Не удалось открыть " + filename);
    f << N << "\n" << std::setprecision(15);
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j)
            f << M[i * N + j] << " ";
        f << "\n";
    }
}

Matrix readMatrix(const std::string& filename, int& N) {
    std::ifstream f(filename);
    if (!f.is_open())
        throw std::runtime_error("Не удалось открыть " + filename);
    f >> N;
    Matrix M(N * N);
    for (int i = 0; i < N * N; ++i)
        if (!(f >> M[i]))
            throw std::runtime_error("Недостаточно данных в " + filename);
    return M;
}

int main(int argc, char* argv[]) {
    int N;
    int num_threads;

    if (argc > 2) {
        N = std::stoi(argv[1]);
        num_threads = std::stoi(argv[2]);
        omp_set_num_threads(num_threads); 
    }
    else {
        std::cout << "Введите N: ";
        std::cin >> N;
        std::cout << "Введите количество потоков: ";
        std::cin >> num_threads;
        omp_set_num_threads(num_threads);
    }

    if (N <= 0) {
        std::cerr << "N должно быть > 0\n";
        return 1;
    }

    try {
        Matrix A(N * N), B(N * N);

        if (N < FILE_WRITE_LIMIT) {
            generateAndWrite("matrixA.txt", N, A);
            generateAndWrite("matrixB.txt", N, B);
        }
        else {
            std::srand(std::time(nullptr) + std::rand());
            for (int i = 0; i < N * N; ++i) {
                A[i] = (double)std::rand() / RAND_MAX;
                B[i] = (double)std::rand() / RAND_MAX;
            }
        }

        Matrix A2, B2;
        if (N < FILE_WRITE_LIMIT) {
            int nA = 0, nB = 0;
            A2 = readMatrix("matrixA.txt", nA);
            B2 = readMatrix("matrixB.txt", nB);
            if (nA != N || nB != N)
                throw std::runtime_error("Размеры в файлах не совпадают");
        }
        else {
            A2 = A;
            B2 = B;
        }

        Matrix C(N * N, 0.0);

        double t0 = omp_get_wtime();

#pragma omp parallel for
        for (int i = 0; i < N; ++i) {
            for (int k = 0; k < N; ++k) {
                double a = A2[i * N + k];
                int row_idx = i * N;
                for (int j = 0; j < N; ++j) {
                    C[row_idx + j] += a * B2[k * N + j];
                }
            }
        }

        
        double t1 = omp_get_wtime();
        double elapsed = t1 - t0;

        if (N < FILE_WRITE_LIMIT) {
            std::ofstream out("result.txt", std::ios::trunc);
            if (!out.is_open())
                throw std::runtime_error("Не удалось открыть result.txt");
            out << N << "\n" << std::setprecision(15);
            for (int i = 0; i < N; ++i) {
                for (int j = 0; j < N; ++j)
                    out << C[i * N + j] << " ";
                out << "\n";
            }
            out << "Время: " << elapsed << " секунд\n";
            out << "Объём задачи: " << (long long)N * N * N << " операций\n";
        }

        std::cout << "Время выполнения: " << elapsed << " секунд\n";
        std::cout << "Потоков использовано: " << num_threads << "\n";
        std::cout << "Объём задачи: " << (long long)N * N * N << " операций\n";

        if (N < FILE_WRITE_LIMIT) {
            std::cout << "Матрицы A и B записаны в файлы.\n";
        }

    }
    catch (const std::exception& e) {
        std::cerr << "Ошибка: " << e.what() << "\n";
        return 1;
    }

    return 0;
}