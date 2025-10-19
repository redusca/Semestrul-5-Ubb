#include <iostream>
#include <chrono>
#include <vector>
#include <thread>

using namespace std;

void generator(vector<int> &V, int n,int max ) {
    for (int i = 0; i < n; i++) {
        V[i] = rand() % max;
    }
}

long long sum(const vector<int> &v1, const vector<int> &v2, vector<int> &v3, int n) {
    auto t0 = chrono::high_resolution_clock::now();
    int sum = 0;
    for (int i = 0; i < n; i++) {
        v3[i] = v1[i] + v2[i];
    }
    auto t1 = chrono::high_resolution_clock::now();
    return chrono::duration_cast<chrono::nanoseconds>(t1 - t0).count();
}

long long runCyclic (const vector<int> A, const vector<int> B, vector<int> &C, int numThreads) {
    vector<thread> threads;
    auto t0 = chrono::high_resolution_clock::now();
    
   
    for (int t = 0; t < numThreads; t++) {
        threads.emplace_back([t, numThreads, &A, &B, &C]() {
            for (size_t i = t; i < A.size(); i += numThreads) {
                C[i] = A[i] + B[i];
            }
        });
    }
    for (auto &th : threads) {
        th.join();
    }
    auto t1 = chrono::high_resolution_clock::now();
    return chrono::duration_cast<chrono::nanoseconds>(t1 - t0).count();
}

long long runBlock (const vector<int> A, const vector<int> B, vector<int> &C, int numThreads) {
    vector<thread> threads;
    auto t0 = chrono::high_resolution_clock::now();
    int n = A.size();
    int blockSize = n / numThreads;
    
    for (int t = 0; t < numThreads; t++) {
        size_t start = t * blockSize;
        size_t end = (t == numThreads - 1) ? n : start + blockSize;
        threads.emplace_back([start, end, &A, &B, &C]() {
            for (size_t i = start; i < end; i++) {
                C[i] = A[i] + B[i];
            }
        });
    }
    for (auto &th : threads) {
        th.join();
    }
    auto t1 = chrono::high_resolution_clock::now();
    return chrono::duration_cast<chrono::nanoseconds>(t1 - t0).count();
}

int main() {
    int n = 1000000, maximum = 50000, p = thread::hardware_concurrency();

    cout << "Number of threads: " << p << "\n";

    vector<int> A(n), B(n), C1(n), C2(n), C3(n);
    generator(A, n, maximum);
    generator(B, n, maximum);

    long long time1 = sum(A, B, C1, n);
    long long time2 = runCyclic(A, B, C2, p);
    long long time3 = runBlock(A, B, C3, p);

    cout << "Time single thread: " << time1 << " ns\n";
    cout << "Time multi thread cyclic: " << time2 << " ns\n";
    cout << "Time multi thread block: " << time3 << " ns\n";

    for (int i = 0; i < n; i++) {
        if (C1[i] != C2[i] || C1[i] != C3[i] || C2[i] != C3[i]) {
            cout << " Inegalitate: " << i << ": " << C1[i] << " " << C2[i] << " " << C3[i] << "\n";
            return -1;
        }
    }

    cout << "All results are correct.\n";

    return 0;
}
