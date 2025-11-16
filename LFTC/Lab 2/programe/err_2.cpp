#include <iostream>

int main() {
    long long  n, r , s=0; 
    std::cin >> n;
    while( n ) { 
        std::cin >> r;
        s += r;
        n--;
    }
    std::cout << s << std::endl;
    return 0;
}