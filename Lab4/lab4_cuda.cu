#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <cstdlib>
#include <cmath>
#include <iomanip>

__global__ void matrixMulKernel(double* A, double* B, double* C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < N && col < N) {
        double sum = 0.0;
        for (int k = 0; k < N; ++k) {
            sum += A[row * N + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

void saveMatrix(const std::string& filename, const std::vector<double>& M, int N) {
    std::ofstream f(filename);
    f << N << "\n" << std::setprecision(15);
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j)
            f << M[i * N + j] << " ";
        f << "\n";
    }
}

int main(int argc, char** argv) {
    int N = (argc > 1) ? std::atoi(argv[1]) : 500;
    int block_size = (argc > 2) ? std::atoi(argv[2]) : 16;

    size_t bytes = N * N * sizeof(double);
    std::vector<double> h_A(N * N), h_B(N * N), h_C(N * N);
    
    for (int i = 0; i < N * N; ++i) {
        h_A[i] = (double)rand() / RAND_MAX;
        h_B[i] = (double)rand() / RAND_MAX;
    }

    // Сохрананение исходных матриц с размером N=200 (для верификации)
    if (N <= 200) {
        saveMatrix("matrixA.txt", h_A, N);
        saveMatrix("matrixB.txt", h_B, N);
    }

    double *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);

    cudaMemcpy(d_A, h_A.data(), bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B.data(), bytes, cudaMemcpyHostToDevice);

    dim3 threadsPerBlock(block_size, block_size);
    dim3 blocksPerGrid((N + block_size - 1) / block_size, (N + block_size - 1) / block_size);

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    
    cudaEventRecord(start);
    matrixMulKernel<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    double seconds = milliseconds / 1000.0;

    cudaMemcpy(h_C.data(), d_C, bytes, cudaMemcpyDeviceToHost);

    if (N <= 200) {
        saveMatrix("result.txt", h_C, N);
    }

    std::cout << "N=" << N << " Block=" << block_size 
              << " Time=" << seconds << " C[0]=" << h_C[0] << std::endl;

    cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
    return 0;
}
