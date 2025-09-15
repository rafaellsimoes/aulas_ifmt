#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n, i, soma = 0;
    int *vetor; 
    char cmdLine[200];

    printf("Digite o tamanho do vetor: ");
    scanf("%d", &n);

    
    vetor = (int *) malloc(n * sizeof(int));
    if (vetor == NULL) {
        printf("Erro ao alocar memoria!\n");
        return 1;
    }


    for (i = 0; i < n; i++) {
        printf("Digite o elemento %d: ", i+1);
        scanf("%d", &vetor[i]);
        soma += vetor[i];
    }

    sprintf(cmdLine, "cmd.exe /c echo Processo filho: soma dos elementos = %d", soma);

    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    // Criar processo filho
    if (!CreateProcessA(
        NULL,           // Nome do executável
        cmdLine,        // Linha de comando
        NULL,           // Segurança do processo
        NULL,           // Segurança da thread
        FALSE,          // Não herdar handles
        0,              // Flags
        NULL,           // Ambiente
        NULL,           // Diretório
        &si,            // Startup info
        &pi             // Process info
    )) {
        printf("Erro ao criar processo: %ld\n", GetLastError());
        free(vetor);
        return 1;
    }

    printf("Processo pai: Criou processo filho com ID %ld\n", pi.dwProcessId);

    WaitForSingleObject(pi.hProcess, INFINITE);
    printf("Processo pai: Processo filho terminou\n");

 
    free(vetor);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    printf("Pressione Enter para sair...");
    getchar(); getchar();

    return 0;
}
