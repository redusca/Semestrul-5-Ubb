#include <iostream>
using namespace std;

int main() {
    int bad1 = 0129;       
    int bad2 = 00x1F;     
    int bad3 = 0b102;     
    int bad4 = +;          
    int bad5 = -0x;        

    int bad6 = 123UU;      
    int bad7 = 45Lu;       
    int bad8 = 100LUL;   
    int bad15 = 100LLL;  

    int bad13 = 0xGHI;    

    int bad14 = 0c1010;
    int bad12 = 012x01;
    int bad1555 = 00000;
 
    return 0;
}
