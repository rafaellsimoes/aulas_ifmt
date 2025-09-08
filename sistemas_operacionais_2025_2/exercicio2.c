#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    int num1, num2;
    char cmdLine[100];

    printf("Digite o primeiro numero: ");
    scanf("%d", &num1);
    
    printf("Digite o segundo numero: ");
    scanf("%d", &num2);
    
    
    while (num2 == 0) {
        printf("Erro: Divisao por zero nao permitida!\n");
        printf("Digite um segundo numero diferente de zero: ");
        scanf("%d", &num2);
    }
    
    
    sprintf(cmdLine, "cmd.exe /c echo Processo filho: %d / %d = %d", 
            num1, num2, num1 / num2);
    
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
        return 1;
    }
    
    printf("Processo pai: Criou processo filho com ID %ld\n", pi.dwProcessId);
    
    
    WaitForSingleObject(pi.hProcess, INFINITE);
    
    printf("Processo pai: Processo filho terminou\n");
    
    
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    
    printf("Pressione Enter para sair...");
    getchar(); getchar(); 
    
    return 0;
}
