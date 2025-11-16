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

vector<char> aduna(const vector<char>& numar1, const vector<char>& numar2) {
    int N1 = numar1.size();
    int N2 = numar2.size();
    int maxN = max(N1, N2);
    
    vector<char> rezultat;
    char carry = 0;
    
    for (int i = 0; i < maxN || carry > 0; i++) {
        char suma = carry;
        
        if (i < N1) {
            suma += numar1[i];
        }
        if (i < N2) {
            suma += numar2[i];
        }
        
        rezultat.push_back(suma % 10);
        carry = suma / 10;
    }
    
    return rezultat;
}

int main() {
    auto start = chrono::high_resolution_clock::now();
    
    vector<char> numar1 = citesteNumar("Numar1.txt");
    vector<char> numar2 = citesteNumar("Numar2.txt");
    vector<char> rezultat = aduna(numar1, numar2);
    
    scrieRezultat("Numar3_var0.txt", rezultat);
    
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> duration = end - start;
    
    cout << "Timp executie secvential: " << duration.count() << " secunde" << endl;
    cout << "Rezultat scris in Numar3.txt" << endl;
    
    return 0;
}
