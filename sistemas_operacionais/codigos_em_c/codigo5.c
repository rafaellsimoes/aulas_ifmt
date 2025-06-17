#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdbool.h>
#include <time.h>

// Configurações
#define QUANTUM 2      // Quantum de tempo (em ticks)
#define TOTAL_TICKS 18 // Tempo total de simulação
#define NUM_TASKS 5   // Número de tarefas

// Estrutura para armazenar métricas de eficiência
typedef struct {
    int task_id;
    int ticks_executados;   // Quantos ticks a tarefa usou
    int trocas_contexto;    // Quantas vezes foi interrompida
    double eficiencia;      // % de ticks úteis (sem overhead)
} TaskMetrics;

// Variáveis globais
TaskMetrics metrics[NUM_TASKS] = {
    {1, 0, 0, 0.0}, // Task 1
    {2, 0, 0, 0.0}  // Task 2
};
volatile int current_task = 0; // Tarefa atual (0 ou 1)
volatile int current_tick = 0; // Contador global de ticks

// Função executada por cada tarefa
void* task_function(void* arg) {
    int task_id = *(int*)arg;
    while (current_tick < TOTAL_TICKS) {
        if (current_task == task_id - 1) { // Verifica se é sua vez
            metrics[task_id - 1].ticks_executados++;
            printf("[TICK %d] Task %d executando...\n", current_tick + 1, task_id);
            usleep(200000); // Simula trabalho (200ms)
        }
    }
    return NULL;
}

// Função do escalonador (chamada a cada quantum)
void scheduler() {
    static int ticks_no_quantum = 0;
    ticks_no_quantum++;

    // Troca de tarefa após o quantum
    if (ticks_no_quantum >= QUANTUM) {
        metrics[current_task].trocas_contexto++;
        current_task = (current_task + 1) % NUM_TASKS;
        ticks_no_quantum = 0;
        printf("[SCHEDULER] Troca de contexto para Task %d\n", current_task + 1);
    }
}

// Calcula a eficiência do sistema
void calculate_efficiency() {
    int total_ticks_uteis = 0;
    int total_trocas = 0;

    for (int i = 0; i < NUM_TASKS; i++) {
        total_ticks_uteis += metrics[i].ticks_executados;
        total_trocas += metrics[i].trocas_contexto;
        metrics[i].eficiencia = (double)metrics[i].ticks_executados / 
                               (metrics[i].ticks_executados + metrics[i].trocas_contexto) * 100;
    }

    double eficiencia_global = (double)total_ticks_uteis / (total_ticks_uteis + total_trocas) * 100;

    printf("\n=== Métricas de Eficiência ===\n");
    printf("Quantum: %d ticks\n", QUANTUM);
    printf("Ticks totais: %d\n", TOTAL_TICKS);
    printf("Ticks úteis: %d\n", total_ticks_uteis);
    printf("Trocas de contexto: %d\n", total_trocas);
    printf("Eficiência global: %.2f%%\n", eficiencia_global);

    for (int i = 0; i < NUM_TASKS; i++) {
        printf("[Task %d] Eficiência: %.2f%%\n", 
               metrics[i].task_id, metrics[i].eficiencia);
    }
}

int main() {
    pthread_t threads[NUM_TASKS];
    int task_ids[NUM_TASKS] = {1, 2};

    printf("=== Simulação de Quantum (%d ticks) ===\n", QUANTUM);

    // Cria as threads (tarefas)
    for (int i = 0; i < NUM_TASKS; i++) {
        pthread_create(&threads[i], NULL, task_function, &task_ids[i]);
    }

    // Loop principal: avança os ticks e chama o escalonador
    while (current_tick < TOTAL_TICKS) {
        current_tick++;
        scheduler();
        usleep(100000); // 100ms por tick (simulação)
    }

    // Finaliza as threads e calcula métricas
    for (int i = 0; i < NUM_TASKS; i++) {
        pthread_cancel(threads[i]); // Encerra as threads
    }
    calculate_efficiency();

    return 0;
}
