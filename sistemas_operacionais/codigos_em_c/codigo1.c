#include <stdio.h>

void func2() {
    printf("Estou em func2()\n");
}

void func1() {
    printf("Estou em func1()\n");
    func2();
}

int main() {
    int i = 0, soma = 1;
    while (i < 20) {
        soma = soma + 1;
        i = i + 1;
        printf("i = %d, soma = %d\n", i, soma);
        
        if (i % 5 == 0) {
            func1(); 
        }
    }
    return 0;
}
