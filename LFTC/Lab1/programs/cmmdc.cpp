#include <iostream>

int main() {
    int a, b, r;
    std::cin >> a >> b;
    if (a == 0) {
        std::cout << b << std::endl;
    }
    else{
        while (b != 0) {
            r = a % b;
            a = b;
            b = r;
        }
        std::cout << a << std::endl;
    }
    return 0;
}