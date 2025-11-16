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
        
        int N = max(N1, N2);
        
        int chunkSize = N / (size - 1);
        int remainder = N % (size - 1);
        
        if (remainder != 0) {
            chunkSize++;
            N = chunkSize * (size - 1);
        }
        
        vector<MPI_Request> sendRequests;
        vector<MPI_Request> recvRequests(size - 1);
        vector<vector<char>> rezultatePartiale(size - 1);
        
        vector<vector<char>> allChunks1;
        vector<vector<char>> allChunks2;
        
        int id_proces_curent = 1;
        
        while (id_proces_curent < size) {
            vector<char> chunk1(chunkSize, 0);
            vector<char> chunk2(chunkSize, 0);
            
            int startPos = (id_proces_curent - 1) * chunkSize;
            
            for (int i = 0; i < chunkSize; i++) {
                int globalPos = startPos + i;
                
                if (globalPos < N) {
                    int digitIndex = N1 - 1 - globalPos;
                    if (digitIndex >= 0) {
                        fin1.seekg(headerPos1 + static_cast<streampos>(digitIndex * 2));
                        int cifra;
                        fin1 >> cifra;
                        chunk1[i] = static_cast<char>(cifra);
                    } else {
                        chunk1[i] = 0;
                    }
                }
            }
            
            for (int i = 0; i < chunkSize; i++) {
                int globalPos = startPos + i;
                
                if (globalPos < N) {
                    int digitIndex = N2 - 1 - globalPos;
                    if (digitIndex >= 0) {
                        fin2.seekg(headerPos2 + static_cast<streampos>(digitIndex * 2));
                        int cifra;
                        fin2 >> cifra;
                        chunk2[i] = static_cast<char>(cifra);
                    } else {
                        chunk2[i] = 0;
                    }
                }
            }
            
            allChunks1.push_back(chunk1);
            allChunks2.push_back(chunk2);
            
            MPI_Request req1, req2;
            MPI_Isend(allChunks1.back().data(), chunkSize, MPI_CHAR, 
                     id_proces_curent, 0, MPI_COMM_WORLD, &req1);
            
            MPI_Isend(allChunks2.back().data(), chunkSize, MPI_CHAR, 
                     id_proces_curent, 1, MPI_COMM_WORLD, &req2);
            
            sendRequests.push_back(req1);
            sendRequests.push_back(req2);
            
            id_proces_curent++;
        }
        
        fin1.close();
        fin2.close();
        
        for (int i = 1; i < size; i++) {
            rezultatePartiale[i - 1].resize(chunkSize);
            MPI_Irecv(rezultatePartiale[i - 1].data(), chunkSize, MPI_CHAR,
                     i, 2, MPI_COMM_WORLD, &recvRequests[i - 1]);
        }
        
        MPI_Waitall(sendRequests.size(), sendRequests.data(), MPI_STATUSES_IGNORE);
        
        MPI_Waitall(recvRequests.size(), recvRequests.data(), MPI_STATUSES_IGNORE);
        
        char finalCarry = 0;
        MPI_Recv(&finalCarry, 1, MPI_CHAR, size - 1, 3, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        
        vector<char> rezultatFinal(N);
        
        for (int i = 1; i < size; i++) {
            int startIdx = (i - 1) * chunkSize;
            for (int j = 0; j < chunkSize && (startIdx + j) < N; j++) {
                rezultatFinal[startIdx + j] = rezultatePartiale[i - 1][j];
            }
        }
        
        while (rezultatFinal.size() > 1 && rezultatFinal.back() == 0) {
            rezultatFinal.pop_back();
        }

        if (finalCarry > 0) {
            rezultatFinal.push_back(finalCarry);
        }
        
        scrieRezultat("Numar3_var3.txt", rezultatFinal);
        
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> duration = end - start;
        
        cout << "Timp executie MPI (Varianta 3 - Asincron): " << duration.count() << " secunde" << endl;
        cout << "Rezultat scris in Numar3_var3.txt" << endl;
        
    } else {
        MPI_Status status;
        MPI_Probe(0, 0, MPI_COMM_WORLD, &status);
        int chunkSize;
        MPI_Get_count(&status, MPI_CHAR, &chunkSize);
        
        vector<char> chunk1(chunkSize);
        vector<char> chunk2(chunkSize);
        
        MPI_Request req1, req2, req3;
        
        MPI_Irecv(chunk1.data(), chunkSize, MPI_CHAR, 0, 0, MPI_COMM_WORLD, &req1);
        
        MPI_Irecv(chunk2.data(), chunkSize, MPI_CHAR, 0, 1, MPI_COMM_WORLD, &req2);
        
        char carryIn = 0;
        if (rank > 1) {
            MPI_Irecv(&carryIn, 1, MPI_CHAR, rank - 1, 3, MPI_COMM_WORLD, &req3);
        }
    
        MPI_Wait(&req1, MPI_STATUS_IGNORE);
        MPI_Wait(&req2, MPI_STATUS_IGNORE);
        
        if (rank > 1) {
            MPI_Wait(&req3, MPI_STATUS_IGNORE);
        }
        
        vector<char> rezultatPartial(chunkSize);
        char carry = carryIn;
        
        for (int i = 0; i < chunkSize; i++) {
            char suma = chunk1[i] + chunk2[i] + carry;
            rezultatPartial[i] = suma % 10;
            carry = suma / 10;
        }
        
        if (rank < size - 1) {
            MPI_Send(&carry, 1, MPI_CHAR, rank + 1, 3, MPI_COMM_WORLD);
        } else {
            MPI_Send(&carry, 1, MPI_CHAR, 0, 3, MPI_COMM_WORLD);
        }
        
        MPI_Request sendReq;
        MPI_Isend(rezultatPartial.data(), chunkSize, MPI_CHAR, 0, 2, MPI_COMM_WORLD, &sendReq);
        
        MPI_Wait(&sendReq, MPI_STATUS_IGNORE);
    }
    
    MPI_Finalize();
    return 0;
}
