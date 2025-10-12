#include <iostream>

int main() {
    long long  n, r , s=0; // long long nu e defenit ca tip de date
    std::cin >> n;
    while( n ) { // while (n) nu este definit in EBNF
        std::cin >> r;
        s += r;
        n--;
    }
    std::cout << s << std::endl;
    return 0;
}