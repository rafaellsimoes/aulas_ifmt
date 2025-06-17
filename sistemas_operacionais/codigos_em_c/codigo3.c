#include <stdio.h>
#include <windows.h>

#define ITERATIONS 5

void sum_process(int process_id) {
    int sum = 0;
    for (int i = 0; i < ITERATIONS; i++) {
        sum += i;
        printf("Processo %d: soma = %d (Iteracao %d)\n", process_id, sum, i);
        Sleep(1000); // Pausa de 1 segundo (em milissegundos)
    }
}

int main() {
    printf("=== Iniciando processos (mudancas de contexto) ===\n");

    STARTUPINFO si = { sizeof(STARTUPINFO) };
    PROCESS_INFORMATION pi;

    // Cria um novo processo
    if (CreateProcess(
        NULL,           // Nome do executável (NULL = usa o mesmo do pai)
        "cmd /c echo Processo filho criado && pause", // Comando simples
        NULL,           // Atributos de segurança do processo
        NULL,           // Atributos de segurança da thread
        FALSE,          // Herança de handles (FALSE = não herda)
        0,              // Flags (0 = padrão)
        NULL,           // Ambiente (NULL = usa o do pai)
        NULL,           // Diretório (NULL = usa o do pai)
        &si,           // STARTUPINFO
        &pi            // PROCESS_INFORMATION
    )) {
        // Processo pai continua executando
        sum_process(1);

        // Espera o processo filho terminar
        WaitForSingleObject(pi.hProcess, INFINITE);

        // Fecha os handles
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    } else {
        printf("Erro ao criar processo (%d)\n", GetLastError());
    }

    printf("=== Todos os processos terminaram ===\n");
    return 0;
}
