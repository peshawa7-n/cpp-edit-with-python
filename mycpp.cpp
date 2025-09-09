#include <iostream>

extern "C" {
    int add(int a, int b) {
        return a + b;
    }

    void say_hello() {
        std::cout << "Hello from C++!" << std::endl;
    }
}

