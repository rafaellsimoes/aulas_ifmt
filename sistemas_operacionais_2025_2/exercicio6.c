#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

#define TAMANHO_VETOR 3

int main() {
    int numeros[TAMANHO_VETOR];
    int soma = 0;
    
    printf("Digite %d numeros:\n", TAMANHO_VETOR);
    for (int i = 0; i < TAMANHO_VETOR; i++) {
        printf("Numero %d: ", i + 1);
        scanf("%d", &numeros[i]);
        soma += numeros[i];
    }
    
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));
    

    char cmdLine[200];
    sprintf_s(cmdLine, sizeof(cmdLine), "cmd.exe /c echo Processo filho: Media dos numeros = %d", 
            soma / TAMANHO_VETOR);
    
    if (!CreateProcessA(
        NULL,           // Nome do executável
        cmdLine,        // Linha de comando
        NULL,           // Segurança do processo
        NULL,           // Segurança da thread
        FALSE,          // Não herdar handles
        CREATE_NEW_CONSOLE, // Criar nova janela de console
        NULL,           // Ambiente
        NULL,           // Diretório
        &si,            // Startup info
        &pi             // Process info
    )) {
        printf("Erro ao criar processo: %ld\n", GetLastError());
        return 1;
    }
    
    printf("\nProcesso pai: Numeros digitados: ");
    for (int i = 0; i < TAMANHO_VETOR; i++) {
        printf("%d ", numeros[i]);
        if (i < TAMANHO_VETOR - 1) printf("+ ");
    }
    printf("= %d\n", soma);
    
    printf("Processo pai: Criou processo filho com ID %ld\n", pi.dwProcessId);
    

    WaitForSingleObject(pi.hProcess, INFINITE);
    
    printf("Processo pai: Processo filho terminou\n");
   
    
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    
    printf("Pressione Enter para sair...");
    getchar(); 
    getchar(); 
    
    return 0;
}
