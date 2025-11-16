#include <mpi.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <algorithm>

using namespace std;

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
    
    if (rank == 0) {
        ifstream fin1("Numar1.txt");
        ifstream fin2("Numar2.txt");
        
        int N1, N2;
        fin1 >> N1;
        fin2 >> N2;
        
        streampos headerPos1 = fin1.tellg();
        streampos headerPos2 = fin2.tellg();
        
        int maxN = max(N1, N2);
        
        int chunkSize = maxN / (size - 1);
        int remainder = maxN % (size - 1);
        
        vector<char> rezultat(maxN + 1, 0);
        
        int currentPos = 0;
        int id_proces_curent = 1;
        
        while (currentPos < maxN && id_proces_curent < size) {
            int currentChunkSize = chunkSize;
            if (id_proces_curent <= remainder) {
                currentChunkSize++;
            }
            
            if (currentPos + currentChunkSize > maxN) {
                currentChunkSize = maxN - currentPos;
            }
            
            vector<char> chunk1(currentChunkSize);
            vector<char> chunk2(currentChunkSize);
            
            for (int i = 0; i < currentChunkSize; i++) {
                int digitIndex = N1 - 1 - (currentPos + i);
                if (digitIndex >= 0) {
                    fin1.seekg(headerPos1 + static_cast<streampos>(digitIndex * 2));
                    int cifra;
                    fin1 >> cifra;
                    chunk1[i] = static_cast<char>(cifra);
                } else {
                    chunk1[i] = 0; 
                }
            }
            
            for (int i = 0; i < currentChunkSize; i++) {
                int digitIndex = N2 - 1 - (currentPos + i); 
                if (digitIndex >= 0) {
                    fin2.seekg(headerPos2 + static_cast<streampos>(digitIndex * 2));
                    int cifra;
                    fin2 >> cifra;
                    chunk2[i] = static_cast<char>(cifra);
                } else {
                    chunk2[i] = 0; 
                }
            }
            
            MPI_Send(&currentChunkSize, 1, MPI_INT, id_proces_curent, 0, MPI_COMM_WORLD);
            MPI_Send(chunk1.data(), currentChunkSize, MPI_CHAR, id_proces_curent, 1, MPI_COMM_WORLD);
            MPI_Send(chunk2.data(), currentChunkSize, MPI_CHAR, id_proces_curent, 2, MPI_COMM_WORLD);
            
            currentPos += currentChunkSize;
            id_proces_curent++;
        }
        
        fin1.close();
        fin2.close();
        
        currentPos = 0;
        char carry = 0;
        
        for (int procId = 1; procId < size; procId++) {
            int currentChunkSize = chunkSize;
            if (procId <= remainder) {
                currentChunkSize++;
            }
            
            if (currentChunkSize == 0 || currentPos >= maxN) {
                continue;
            }
            
            if (currentPos + currentChunkSize > maxN) {
                currentChunkSize = maxN - currentPos;
            }
            
            vector<char> partialResult(currentChunkSize);
            MPI_Recv(partialResult.data(), currentChunkSize, MPI_CHAR, procId, 3, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            
            if (procId == size - 1) {
                MPI_Recv(&carry, 1, MPI_CHAR, procId, 4, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }
            
            for (int i = 0; i < currentChunkSize; i++) {
                rezultat[currentPos + i] = partialResult[i];
            }
            
            currentPos += currentChunkSize;
        }
        
        if (carry > 0) {
            rezultat[maxN] = carry;
        } else {
            rezultat.resize(maxN);
        }
        
        scrieRezultat("Numar3_var1.txt", rezultat);
        
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> duration = end - start;
        
        cout << "Timp executie MPI (Varianta 1): " << duration.count() << " secunde" << endl;
        cout << "Rezultat scris in Numar3.txt" << endl;
        
    } else {
        int chunkSize;
        MPI_Recv(&chunkSize, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        
        if (chunkSize > 0) {
            vector<char> chunk1(chunkSize);
            vector<char> chunk2(chunkSize);
            
            MPI_Recv(chunk1.data(), chunkSize, MPI_CHAR, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Recv(chunk2.data(), chunkSize, MPI_CHAR, 0, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            
            vector<char> rezultatPartial_without_carry(chunkSize);
            vector<char> rezultatPartial(chunkSize);

            char carry_w = 0;
            for (int i = 0; i < chunkSize; i++) {
                char suma = chunk1[i] + chunk2[i] + carry_w;
                rezultatPartial_without_carry[i] = suma % 10;
                carry_w = suma / 10;
            }
            char carry = 1;
            for (int i = 0; i < chunkSize; i++) {
                char suma = chunk1[i] + chunk2[i] + carry;
                rezultatPartial[i] = suma % 10;
                carry = suma / 10;
            }

            char real_carry;
            if (rank > 1) {
                MPI_Recv(&real_carry, 1, MPI_CHAR, rank - 1, 5, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }

            if(real_carry != 1) {
                rezultatPartial = rezultatPartial_without_carry;
                carry = carry_w;
            }
            
            if (rank < size - 1) {
                MPI_Send(&carry, 1, MPI_CHAR, rank + 1, 5, MPI_COMM_WORLD);
            }
            
            if (rank == size - 1) {
                MPI_Send(&carry, 1, MPI_CHAR, 0, 4, MPI_COMM_WORLD);
            }
            
            MPI_Send(rezultatPartial.data(), chunkSize, MPI_CHAR, 0, 3, MPI_COMM_WORLD);
        }
    }
    
    MPI_Finalize();
    return 0;
}
