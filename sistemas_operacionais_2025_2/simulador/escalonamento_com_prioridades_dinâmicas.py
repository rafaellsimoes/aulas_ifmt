class Tarefa:
    def __init__(self, nome, tempo_chegada, duracao, prioridade=None):
        self.nome = nome
        self.tempo_chegada = tempo_chegada
        self.duracao = duracao
        self.tempo_restante = duracao
        self.prioridade = prioridade or 0
        self.tempo_inicio = None
        self.tempo_fim = None
        self.tempo_espera = 0


def escalonamento_prioridades_dinamicas(tarefas, quantum, incremento_espera=1, reducao_execucao=2):
    """
    Escalonamento com prioridades dinâmicas (preemptivo):
    - Cada tarefa ganha prioridade enquanto espera.
    - Cada tarefa perde prioridade enquanto executa.
    - A execução é limitada por um quantum definido.
    """

   
    tarefas_copia = [
        Tarefa(t.nome, t.tempo_chegada, t.duracao, t.prioridade)
        for t in tarefas
    ]

    tempo_atual = 0
    fila_prontos = []
    completadas = 0
    n = len(tarefas_copia)
    tarefas_agendadas = []
    tarefas_ordenadas = sorted(tarefas_copia, key=lambda x: x.tempo_chegada)
    indice_tarefa = 0

    while completadas < n:
      
        while indice_tarefa < n and tarefas_ordenadas[indice_tarefa].tempo_chegada <= tempo_atual:
            fila_prontos.append(tarefas_ordenadas[indice_tarefa])
            indice_tarefa += 1

     
        for tarefa in fila_prontos:
            if tarefa.tempo_restante > 0:
                tarefa.prioridade += incremento_espera

        if fila_prontos:
            
            fila_prontos.sort(key=lambda x: (-x.prioridade, x.tempo_chegada))
            tarefa = fila_prontos.pop(0)

            if tarefa.tempo_inicio is None:
                tarefa.tempo_inicio = tempo_atual

       
            tempo_execucao = min(quantum, tarefa.tempo_restante)
            tarefa.tempo_restante -= tempo_execucao
            tempo_atual += tempo_execucao

            
            tarefa.prioridade = max(0, tarefa.prioridade - reducao_execucao)

      
            while indice_tarefa < n and tarefas_ordenadas[indice_tarefa].tempo_chegada <= tempo_atual:
                fila_prontos.append(tarefas_ordenadas[indice_tarefa])
                indice_tarefa += 1

            if tarefa.tempo_restante > 0:
                
                fila_prontos.append(tarefa)
            else:
    
                tarefa.tempo_fim = tempo_atual
                tarefa.tempo_espera = tarefa.tempo_fim - tarefa.tempo_chegada - tarefa.duracao
                tarefas_agendadas.append(tarefa)
                completadas += 1
        else:
            tempo_atual += 1

    return tarefas_agendadas


def calcular_metricas(tarefas_agendadas):
    n = len(tarefas_agendadas)
    tempo_total_retorno = sum(t.tempo_fim - t.tempo_chegada for t in tarefas_agendadas)
    tempo_total_espera = sum(t.tempo_espera for t in tarefas_agendadas)
    return tempo_total_retorno / n, tempo_total_espera / n


def mostrar_agendamento(tarefas_agendadas, nome_algoritmo):
    print(f"\n=== {nome_algoritmo} ===")
    print("Tarefa | Chegada | Duração | Início | Fim | Turnaround | Espera | Prioridade final")
    print("-" * 80)
    for t in tarefas_agendadas:
        turnaround = t.tempo_fim - t.tempo_chegada
        print(f"{t.nome:6} | {t.tempo_chegada:7} | {t.duracao:7} | {t.tempo_inicio:6} | {t.tempo_fim:3} | {turnaround:10} | {t.tempo_espera:5} | {t.prioridade:5}")


if __name__ == "__main__":

    tarefas = [
        Tarefa("T1", 0, 8, 1),
        Tarefa("T2", 1, 4, 2),
        Tarefa("T3", 2, 9, 1),
        Tarefa("T4", 3, 5, 3),
        Tarefa("T5", 4, 2, 2)
    ]

    quantum = 2
    resultado = escalonamento_prioridades_dinamicas(tarefas, quantum)

    mostrar_agendamento(resultado, f"Prioridades Dinâmicas (quantum={quantum})")
    turnaround, espera = calcular_metricas(resultado)
    print(f"\nTempo médio de turnaround: {turnaround:.2f}")
    print(f"Tempo médio de espera: {espera:.2f}")
