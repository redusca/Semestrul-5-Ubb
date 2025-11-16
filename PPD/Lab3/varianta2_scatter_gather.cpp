#include <mpi.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <algorithm>

using namespace std;

vector<char> citesteNumar(const string& numeFisier) {
    ifstream fin(numeFisier);
    int N;
    fin >> N;
    
    vector<char> numar(N);
    for (int i = N - 1; i >= 0; i--) {
        int cifra;
        fin >> cifra;
        numar[i] = static_cast<char>(cifra);
    }
    
    fin.close();
    return numar;
}

void scrieRezultat(const string& numeFisier, const vector<char>& rezultat) {
    ofstream fout(numeFisier);
    fout << rezultat.size() << endl;
    
    for (int i = rezultat.size() - 1; i >= 0; i--) {
        fout << static_cast<int>(rezultat[i]);
        if (i > 0) fout << " ";
    }
    fout << endl;
    fout.close();
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    auto start = chrono::high_resolution_clock::now();
    
    int N = 0;
    int chunkSize = 0;
    
    if (rank == 0) {
        vector<char> numar1 = citesteNumar("Numar1.txt");
        vector<char> numar2 = citesteNumar("Numar2.txt");
        
        int N1 = numar1.size();
        int N2 = numar2.size();
        N = max(N1, N2);
        
        if (N % size != 0) {
            N = ((N / size) + 1) * size;
        }
        
        numar1.resize(N, 0);
        numar2.resize(N, 0);
        
        chunkSize = N / size;
        
        MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&chunkSize, 1, MPI_INT, 0, MPI_COMM_WORLD);
        
        vector<char> chunk1(chunkSize);
        vector<char> chunk2(chunkSize);
        
        MPI_Scatter(numar1.data(), chunkSize, MPI_CHAR,
                    chunk1.data(), chunkSize, MPI_CHAR,
                    0, MPI_COMM_WORLD);
        
        MPI_Scatter(numar2.data(), chunkSize, MPI_CHAR,
                    chunk2.data(), chunkSize, MPI_CHAR,
                    0, MPI_COMM_WORLD);
        
        // Procesul 0 calculeaza suma pentru chunk-ul sau
        vector<char> rezultatPartial(chunkSize);
        char carry = 0;
        
        for (int i = 0; i < chunkSize; i++) {
            char suma = chunk1[i] + chunk2[i] + carry;
            rezultatPartial[i] = suma % 10;
            carry = suma / 10;
        }
        
        if (size > 1) {
            MPI_Send(&carry, 1, MPI_CHAR, 1, 0, MPI_COMM_WORLD);
        }
        
        vector<char> rezultatFinal(N);
        MPI_Gather(rezultatPartial.data(), chunkSize, MPI_CHAR,
                   rezultatFinal.data(), chunkSize, MPI_CHAR,
                   0, MPI_COMM_WORLD);
        
        char finalCarry = 0;
        if (size > 1) {
            MPI_Recv(&finalCarry, 1, MPI_CHAR, size - 1, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            if (finalCarry > 0) {
                rezultatFinal.push_back(finalCarry);
            }
        }
        
        while (rezultatFinal.size() > 1 && rezultatFinal.back() == 0) {
            rezultatFinal.pop_back();
        }
        
        scrieRezultat("Numar3_var2.txt", rezultatFinal);
        
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> duration = end - start;
        
        cout << "Timp executie MPI (Varianta 2 - Scatter/Gather): " << duration.count() << " secunde" << endl;
        cout << "Rezultat scris in Numar3.txt" << endl;
        
    } else {
        MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&chunkSize, 1, MPI_INT, 0, MPI_COMM_WORLD);
        
        vector<char> chunk1(chunkSize);
        vector<char> chunk2(chunkSize);
        
        MPI_Scatter(nullptr, chunkSize, MPI_CHAR,
                    chunk1.data(), chunkSize, MPI_CHAR,
                    0, MPI_COMM_WORLD);
        
        MPI_Scatter(nullptr, chunkSize, MPI_CHAR,
                    chunk2.data(), chunkSize, MPI_CHAR,
                    0, MPI_COMM_WORLD);
        
        vector<char> rezultatPartial(chunkSize);
        char carry = 0;

        MPI_Recv(&carry, 1, MPI_CHAR, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        
        for (int i = 0; i < chunkSize; i++) {
            char suma = chunk1[i] + chunk2[i] + carry;
            rezultatPartial[i] = suma % 10;
            carry = suma / 10;
        }
        
        if (rank < size - 1) {
            MPI_Send(&carry, 1, MPI_CHAR, rank + 1, 0, MPI_COMM_WORLD);
        } else {
            MPI_Send(&carry, 1, MPI_CHAR, 0, 1, MPI_COMM_WORLD);
        }
        
        MPI_Gather(rezultatPartial.data(), chunkSize, MPI_CHAR,
                   nullptr, chunkSize, MPI_CHAR,
                   0, MPI_COMM_WORLD);
    }
    
    MPI_Finalize();
    return 0;
}
