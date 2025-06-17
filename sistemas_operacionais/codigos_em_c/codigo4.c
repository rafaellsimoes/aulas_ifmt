#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdbool.h>

// Estrutura do TCB (Task Control Block)
typedef struct {
    int id;
    int tick_count;
    bool is_running;
} TCB;

// Variáveis globais (simulando hardware e sistema)
TCB tcb_A = {1, 0, false};
TCB tcb_B = {2, 0, false};
volatile int current_tick = 0; // Simula um timer de hardware
volatile bool scheduler_activated = false;

// Função do "timer de hardware" (simulado)
void* hardware_timer(void* arg) {
    while (true) {
        sleep(1); // 1 segundo = 1 tick
        current_tick++;
        printf("\n[TICK %d] Hardware timer interrompe a CPU.\n", current_tick);
        scheduler_activated = true; // Ativa o scheduler
    }
    return NULL;
}

// Função do escalonador (scheduler)
void scheduler() {
    if (tcb_A.is_running) {
        tcb_A.is_running = false;
        tcb_B.is_running = true;
        printf("[SCHEDULER] Trocando de Task A para Task B.\n");
    } else {
        tcb_A.is_running = true;
        tcb_B.is_running = false;
        printf("[SCHEDULER] Trocando de Task B para Task A.\n");
    }
}

// Função do dispatcher (prepara contexto da próxima tarefa)
void dispatcher() {
    if (tcb_A.is_running) {
        printf("[DISPATCHER] Restaurando contexto da Task A (TCB %d).\n", tcb_A.id);
    } else {
        printf("[DISPATCHER] Restaurando contexto da Task B (TCB %d).\n", tcb_B.id);
    }
}

// Função da Task A
void* task_A(void* arg) {
    while (true) {
        if (tcb_A.is_running) {
            tcb_A.tick_count++;
            printf("[TASK A] Executando (Tick %d).\n", tcb_A.tick_count);
            sleep(1); // Simula trabalho
        }
    }
    return NULL;
}

// Função da Task B
void* task_B(void* arg) {
    while (true) {
        if (tcb_B.is_running) {
            tcb_B.tick_count++;
            printf("[TASK B] Executando (Tick %d).\n", tcb_B.tick_count);
            sleep(1); // Simula trabalho
        }
    }
    return NULL;
}

// Função principal
int main() {
    pthread_t thread_A, thread_B, thread_timer;

    printf("=== SIMULAÇÃO DE TROCA DE CONTEXTO ===\n");

    // Inicia as threads (tasks e timer)
    pthread_create(&thread_A, NULL, task_A, NULL);
    pthread_create(&thread_B, NULL, task_B, NULL);
    pthread_create(&thread_timer, NULL, hardware_timer, NULL);

    // Loop principal do sistema operacional
    while (true) {
        if (scheduler_activated) {
            printf("\n[INTERRUPT HANDLER] Interrupção recebida.\n");
            printf("[SYSTEM] Salvando contexto da tarefa atual.\n");

            scheduler();          // Decide qual tarefa executar
            dispatcher();        // Prepara o contexto da próxima tarefa
            scheduler_activated = false; // Reseta o flag

            printf("[SYSTEM] Troca de contexto concluída.\n");
        }
    }

    return 0;
}
