#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char nome[50];
    float nota;
} Aluno;

int main() {
    int n = 3, i;
    float soma = 0, media;
    Aluno *turma;
    char cmdLine[200];

    
    while (getchar() != '\n');

    if (n < 0) {
        printf("Quantidade invalida de alunos!\n");
        return 1;
    }

    turma = (Aluno *) malloc(n * sizeof(Aluno));
    if (turma == NULL) {
        printf("Erro ao alocar memoria!\n");
        return 1;
    }

    for (i = 0; i < n; i++) {
        printf("\nDigite o nome do aluno %d: ", i + 1);
        fgets(turma[i].nome, 50, stdin);
        
        size_t len = strlen(turma[i].nome);
        if (len > 0 && turma[i].nome[len - 1] == '\n') {
            turma[i].nome[len - 1] = '\0';
        }

        printf("Digite a nota do aluno %d: ", i + 1);
        scanf("%f", &turma[i].nota);
        while (getchar() != '\n');
        soma += turma[i].nota;
    }

    media = soma / n;
    sprintf(cmdLine, "cmd.exe /c echo Processo filho: Media da turma = %.2f", media);
    
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    if (!CreateProcessA(NULL,
                        cmdLine,
                         NULL,
                         NULL,
                         FALSE,
                         0,
                         NULL,
                         NULL, 
                         &si, 
                         &pi)) {
        printf("Erro ao criar processo: %ld\n", GetLastError());
        free(turma);
        return 1;
    }

    printf("\nProcesso pai: Criou processo filho com ID %ld\n", pi.dwProcessId);
    
    WaitForSingleObject(pi.hProcess, INFINITE);
    printf("Processo pai: Processo filho terminou\n");
    
    free(turma);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    printf("Pressione Enter para sair...");
    getchar();

    return 0;
}
