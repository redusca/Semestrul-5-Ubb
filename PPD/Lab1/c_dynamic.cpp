#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <thread>
#include <vector>

using namespace std;

class Convolutie {

    unsigned int **C;
    unsigned int **matrice;
    unsigned int **matrice_rez;
    unsigned int n, m, k;

    public:
    Convolutie(string input = "date.txt") {
        ifstream f(input);
        if (!f.is_open()) {
            cerr << "Error opening file: " << input << endl;
            exit(1);
        }
        
        f >> k;
        C = new unsigned int*[k];
        for (int i = 0; i < k; i++) {
            C[i] = new unsigned int[k];
            for (int j = 0; j < k; j++) {
                f >> C[i][j];
            }
        }

        f >> n >> m;
        
        matrice = new unsigned int*[n + 1];
        for (int i = 0; i <= n; i++) {
            matrice[i] = new unsigned int[m + 1];
        }
        
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                f >> matrice[i][j];
            }
        }
        
        matrice_rez = new unsigned int*[n + 1];
        for (int i = 0; i <= n; i++) {
            matrice_rez[i] = new unsigned int[m + 1];
        }
        
        f.close();
    }
    
    ~Convolutie() {
        for (int i = 0; i < k; i++) {
            delete[] C[i];
        }
        delete[] C;
        
        for (int i = 0; i <= n; i++) {
            delete[] matrice[i];
        }
        delete[] matrice;
        
        for (int i = 0; i <= n; i++) {
            delete[] matrice_rez[i];
        }
        delete[] matrice_rez;
    }

    unsigned int claim(int x, int y) {
        return matrice[x >= 1 ? (x <= n ? x : n) : 1][y >= 1 ? (y <= m ? y : m) : 1];
    }

    unsigned int conv(int i, int j) {
        unsigned int sum = 0;
        int lim = k / 2;
        for (int x = -lim; x <= lim; x++) {
            for (int y = -lim; y <= lim; y++) {
                sum += claim(i + x, j + y) * C[x + lim][y + lim];
            }
        }
        return sum;
    }

    void secvential() {
        auto start = chrono::high_resolution_clock::now();

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                matrice_rez[i][j] = conv(i, j);
            }
        }

        auto end = chrono::high_resolution_clock::now();
        auto ns = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
        cout << ns << endl;
        
        ofstream g("output/sec/outputCD_" + to_string(k) + "_" + to_string(n) + "_" + to_string(m) + ".txt");
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                g << matrice_rez[i][j] << " ";
            }
            g << "\n";
        }
        g.close();
    }

    void parallel_orz(int threads) {
        auto start = chrono::high_resolution_clock::now();

        vector<thread> thread_pool;
        int rows_per_thread = n / threads;

        for (int t = 0; t < threads; t++) {
            int start_row = t * rows_per_thread + 1;
            int end_row = (t == threads - 1) ? n : (t + 1) * rows_per_thread;

            thread_pool.emplace_back([=]() {
                for (int i = start_row; i <= end_row; i++) {
                    for (int j = 1; j <= m; j++) {
                        matrice_rez[i][j] = conv(i, j);
                    }
                }
            });
        }

        for (auto& th : thread_pool) {
            th.join();
        }

        auto end = chrono::high_resolution_clock::now();
        auto ns = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
        cout << ns << endl;

        ofstream g("output/po/outputCD_" + to_string(k) + "_" + to_string(n) + "_" + to_string(m) + ".txt");
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                g << matrice_rez[i][j] << " ";
            }
            g << "\n";
        }
        g.close();
    }

    void parallel_ver(int threads) {
        auto start = chrono::high_resolution_clock::now();

        vector<thread> thread_pool;
        int cols_per_thread = m / threads;

        for (int t = 0; t < threads; t++) {
            int start_col = t * cols_per_thread + 1;
            int end_col = (t == threads - 1) ? m : (t + 1) * cols_per_thread;

            thread_pool.emplace_back([=]() {
                for (int i = 1; i <= n; i++) {
                    for (int j = start_col; j <= end_col; j++) {
                        matrice_rez[i][j] = conv(i, j);
                    }
                }
            });
        }

        for (auto& th : thread_pool) {
            th.join();
        }

        auto end = chrono::high_resolution_clock::now();
        auto ns = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
        cout << ns << endl;

        ofstream g("output/pv/outputCD_" + to_string(k) + "_" + to_string(n) + "_" + to_string(m) + ".txt");
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                g << matrice_rez[i][j] << " ";
            }
            g << "\n";
        }
        g.close();
    }

    void run(int caz, int threads) {
        if (caz == 1) 
            this->secvential();
        else if (caz == 2)
            this->parallel_orz(threads);
        else if (caz == 3)
            this->parallel_ver(threads);
    }
};

int main(int argc, char** argv) {
    if (argc < 4) {
        cerr << "Usage: " << argv[0] << " <input_file> <threads> <mode>" << endl;
        return 1;
    }
    
    int p = stoi(argv[2]);
    Convolutie* conv = new Convolutie(argv[1]);

    conv->run(stoi(argv[3]), p);

    delete conv;
    return 0;
}