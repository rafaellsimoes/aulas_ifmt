#include <stdio.h>
#include <stdlib.h>

// Estrutura para representar um processo/contexto
typedef struct {
    int id;
    int pc;  // contador de programa simulado
    int i;
    int soma;
} Processo;

// Pilha de processos (simulação)
Processo pilha[10];
int topo_pilha = -1;

// Função para empilhar um processo
void empilhar_processo(int id, int pc, int i, int soma) {
    if (topo_pilha >= 9) {
        printf("Estouro de pilha!\n");
        exit(1);
    }
    topo_pilha++;
    pilha[topo_pilha].id = id;
    pilha[topo_pilha].pc = pc;
    pilha[topo_pilha].i = i;
    pilha[topo_pilha].soma = soma;
}

// Função para desempilhar um processo
Processo desempilhar_processo() {
    if (topo_pilha < 0) {
        printf("Pilha vazia!\n");
        exit(1);
    }
    return pilha[topo_pilha--];
}

// Função para imprimir a pilha atual
void imprimir_pilha() {
    printf("\n--- Pilha de Processos ---\n");
    for (int j = topo_pilha; j >= 0; j--) {
        printf("Nível %d: Processo %d (PC=%d, i=%d, soma=%d)\n", 
               topo_pilha - j, pilha[j].id, pilha[j].pc, pilha[j].i, pilha[j].soma);
    }
    printf("-------------------------\n\n");
}

// Funções simulando diferentes níveis de chamada
void func3(int proc_id) {
    empilhar_processo(proc_id, 3, 0, 0);
    printf("Processo %d: Executando func3()\n", proc_id);
    imprimir_pilha();
    desempilhar_processo();
}

void func2(int proc_id) {
    empilhar_processo(proc_id, 2, 0, 0);
    printf("Processo %d: Executando func2()\n", proc_id);
    imprimir_pilha();
    func3(proc_id);
    desempilhar_processo();
}

void func1(int proc_id) {
    empilhar_processo(proc_id, 1, 0, 0);
    printf("Processo %d: Executando func1()\n", proc_id);
    imprimir_pilha();
    func2(proc_id);
    desempilhar_processo();
}

// Função principal que simula múltiplos processos
void processo_principal(int id) {
    empilhar_processo(id, 0, 0, 1);
    
    while (pilha[topo_pilha].i < 20) {
        pilha[topo_pilha].soma++;
        pilha[topo_pilha].i++;
        
        printf("Processo %d: i = %d, soma = %d\n", 
               id, pilha[topo_pilha].i, pilha[topo_pilha].soma);
        
        if (pilha[topo_pilha].i % 5 == 0) {
            func1(id);
        }
        
        imprimir_pilha();
        
        // Simulação de troca de contexto
        if (pilha[topo_pilha].i % 7 == 0) {
            printf("\n=== TROCA DE CONTEXTO ===\n");
            Processo p = desempilhar_processo();
            empilhar_processo(p.id, p.pc, p.i, p.soma);
        }
    }
    
    desempilhar_processo();
}

int main() {
    printf("=== SIMULAÇÃO DE PILHA DE PROCESSOS ===\n");
    
    // Simula dois processos alternando
    for (int ciclo = 0; ciclo < 2; ciclo++) {
        printf("\n>>> Ciclo de Execução %d <<<\n", ciclo+1);
        processo_principal(1);  // Processo 1
        processo_principal(2);  // Processo 2
    }
    
    return 0;
}
