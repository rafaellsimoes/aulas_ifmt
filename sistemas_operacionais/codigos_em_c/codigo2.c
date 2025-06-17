#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>

void ListProcesses() {
    HANDLE hProcessSnap;
    PROCESSENTRY32 pe32;

    // Tirar um "snapshot" dos processos
    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hProcessSnap == INVALID_HANDLE_VALUE) {
        printf("Erro ao criar snapshot.\n");
        return;
    }

    pe32.dwSize = sizeof(PROCESSENTRY32);

    // Listar o primeiro processo
    if (!Process32First(hProcessSnap, &pe32)) {
        printf("Erro ao listar processos.\n");
        CloseHandle(hProcessSnap);
        return;
    }

    printf("PID\t\tNome do Processo\n");
    printf("--------------------------------\n");

    // Iterar sobre todos os processos
    do {
        printf("%-8d\t%s\n", pe32.th32ProcessID, pe32.szExeFile);
    } while (Process32Next(hProcessSnap, &pe32));

    CloseHandle(hProcessSnap);
}

int main() {
    printf("=== Contexto das Tarefas (Processos Windows) ===\n");
    ListProcesses();
    return 0;
}
