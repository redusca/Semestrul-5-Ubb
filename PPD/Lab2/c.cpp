#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <thread>
#include <vector>
#include <syncstream>
#include <barrier>

using namespace std;

class Convolutie
{
    int **C;
    int **matrice;
    int n, m, k;

public:
    Convolutie(string input = "date.txt")
    {
        ifstream f(input);
        if (!f.is_open())
        {
            cerr << "Error opening file: " << input << endl;
            exit(1);
        }

        f >> k;
        C = new int *[k];
        for (int i = 0; i < k; i++)
        {
            C[i] = new int[k];
            for (int j = 0; j < k; j++)
            {
                f >> C[i][j];
            }
        }

        f >> n >> m;

        matrice = new int *[n + 1];
        for (int i = 0; i <= n; i++)
        {
            matrice[i] = new int[m + 1];
        }

        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= m; j++)
            {
                f >> matrice[i][j];
            }
        }

        f.close();
    }

    ~Convolutie()
    {
        for (int i = 0; i < k; i++)
        {
            delete[] C[i];
        }
        delete[] C;

        for (int i = 0; i <= n; i++)
        {
            delete[] matrice[i];
        }
        delete[] matrice;
    }

    int claim(int x, int y)
    {
        return matrice[x >= 1 ? (x <= n ? x : n) : 1][y >= 1 ? (y <= m ? y : m) : 1];
    }

    int conv(int i, int j)
    {
        int sum = 0;
        int lim = k / 2;
        for (int x = -lim; x <= lim; x++)
        {
            for (int y = -lim; y <= lim; y++)
            {
                sum += claim(i + x, j + y) * C[x + lim][y + lim];
            }
        }
        return sum;
    }

    int conv_vec(int j,int* a,int* b,int* c){
        int sum = 0;
        for (int x = -1; x <= 1 ; x++)
        {
            for (int y = -1; y <= 1; y++)
            {
                int coeff = C[x + 1][y + 1];
                int x_val = (x == -1) ? a[j + y] : (x == 0) ? b[j + y] : c[j + y];
                sum += x_val * coeff;
            }
        }
        return sum;
    }

    void init_vec(int* a,int* b,int* c,int i){
        for (int j = 0; j <= m+1; j++) {
            a[j] = claim(i-1, j);
            b[j] = claim(i, j);
            c[j] = claim(i+1, j);
        }
    }

    void next_vec(int* a,int* b,int* c,int i){
        for (int j = 0; j <= m+1; j++) {
            a[j] = b[j];
            b[j] = c[j];
            c[j] = claim(i+1, j);
        }
    }

    void secvential() {
        auto start = chrono::high_resolution_clock::now();

        int *a = new int[m + 2];
        int *b = new int[m + 2];
        int *c = new int[m + 2];
        this->init_vec(a, b, c, 1);

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                matrice[i][j] = conv_vec(j, a, b, c);
            }
            this->next_vec(a, b, c, i + 1);
        }

        delete[] a;
        delete[] b;
        delete[] c;
        
        auto end = chrono::high_resolution_clock::now();
        auto ns = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
        cout << ns << endl;
        
        ofstream g("output/sec/outputC_" + to_string(k) + "_" + to_string(n) + "_" + to_string(m) + ".txt");
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                g << matrice[i][j] << " ";
            }
            g << "\n";
        }
        g.close();
    }

    void parallel(int threads)
    {
        auto start = chrono::high_resolution_clock::now();

        vector<thread> thread_pool;
        int rows_per_thread = n / threads;
        int max_rows = n - (threads - 1) * rows_per_thread; // Max rows for last thread

        vector<int*> safe_vec(threads-1);
        for (int t = 1; t < threads; t++) {
            safe_vec[t-1] = new int[m+2];
            for(int j=0;j<=m+1;j++)
                safe_vec[t-1][j] = claim(t*rows_per_thread+1, j);
        }
            
        // Create a barrier that waits for all threads before proceeding to next row
        barrier sync_barrier(threads);

        for (int t = 0; t < threads; t++)
        {
            int start_row = t * rows_per_thread + 1;
            int end_row = (t == threads - 1) ? n : (t + 1) * rows_per_thread;
            
            thread_pool.emplace_back([=, &sync_barrier](){
                int * a = new int[m+2];
                int * b = new int[m+2];
                int * c = new int[m+2];
                this->init_vec(a, b, c, start_row);
                
                // All threads must iterate the same number of times for barrier synchronization
                for (int iter = 0; iter < max_rows; iter++) {
                    int i = start_row + iter;
                    
                    // Only process if within this thread's range
                    if (i <= end_row) {
                        for (int j = 1; j <= m; j++) {
                            matrice[i][j] = conv_vec(j, a, b, c);
                        }
                    }
                    
                    // Wait for all threads to finish their current row
                    sync_barrier.arrive_and_wait();
                    
                    // Only advance vectors if within range
                    if (i <= end_row) {
                        this->next_vec(a, b, c, i + 1);
                        if(t < threads -1 && i == end_row-1)
                           c = safe_vec[t];
                    }
                }
                
                delete[] a;
                delete[] b;
                delete[] c;}
            );
                
        }
        
        for (auto &th : thread_pool)
        {
            th.join();
        }

        auto end = chrono::high_resolution_clock::now();
        auto ns = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
        cout << ns << endl;

        ofstream g("output/p/outputC_" + to_string(k) + "_" + to_string(n) + "_" + to_string(m) + ".txt");
        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= m; j++)
            {
                g << matrice[i][j] << " ";
            }
            g << "\n";
        }
        g.close();
    }

    void run(int caz, int threads)
    {
        if (caz == 1)
            this->secvential();
        else if (caz == 2)
            this->parallel(threads);
    }
};

int main(int argc, char **argv)
{
    if (argc < 4)
    {
        cerr << "Usage: " << argv[0] << " <input_file> <threads> <mode>" << endl;
        return 1;
    }

    int p = stoi(argv[2]);
    Convolutie *conv = new Convolutie(argv[1]);

    conv->run(stoi(argv[3]),p);

    delete conv;
    return 0;
}