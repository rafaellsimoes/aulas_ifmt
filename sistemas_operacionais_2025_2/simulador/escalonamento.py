class Tarefa:
    def __init__(self, nome, tempo_chegada, duracao, prioridade=None):
        self.nome = nome
        self.tempo_chegada = tempo_chegada
        self.duracao = duracao
        self.tempo_restante = duracao
        self.prioridade = prioridade
        self.tempo_inicio = None
        self.tempo_fim = None
        self.tempo_espera = 0

def escalonamento_fcfs(tarefas):
    tarefas_ordenadas = sorted(tarefas, key=lambda x: x.tempo_chegada)
    tempo_atual = 0
    tarefas_agendadas = []
    
    for tarefa in tarefas_ordenadas:
        if tempo_atual < tarefa.tempo_chegada:
            tempo_atual = tarefa.tempo_chegada
        
        tarefa.tempo_inicio = tempo_atual
        tarefa.tempo_fim = tempo_atual + tarefa.duracao
        tarefa.tempo_espera = tempo_atual - tarefa.tempo_chegada
        tempo_atual = tarefa.tempo_fim
        tarefas_agendadas.append(tarefa)
    
    return tarefas_agendadas

def escalonamento_sjf(tarefas):
    tarefas_ordenadas = sorted(tarefas, key=lambda x: x.tempo_chegada)
    tempo_atual = 0
    tarefas_agendadas = []
    fila_prontos = []
    completadas = 0
    n = len(tarefas)
    
    while completadas < n:
        for tarefa in tarefas_ordenadas:
            if tarefa.tempo_chegada <= tempo_atual and tarefa not in fila_prontos and tarefa not in tarefas_agendadas:
                fila_prontos.append(tarefa)
        
        if fila_prontos:
            fila_prontos.sort(key=lambda x: x.duracao)
            tarefa = fila_prontos.pop(0)
            
            tarefa.tempo_inicio = tempo_atual
            tarefa.tempo_fim = tempo_atual + tarefa.duracao
            tarefa.tempo_espera = tempo_atual - tarefa.tempo_chegada
            tempo_atual = tarefa.tempo_fim
            tarefas_agendadas.append(tarefa)
            completadas += 1
        else:
            tempo_atual += 1
    
    return tarefas_agendadas

def escalonamento_srtf(tarefas):
    tarefas_copia = [Tarefa(tarefa.nome, tarefa.tempo_chegada, tarefa.duracao, tarefa.prioridade) for tarefa in tarefas]
    tempo_atual = 0
    tarefas_agendadas = []
    completadas = 0
    n = len(tarefas_copia)
    tarefa_atual = None
    
    while completadas < n:
        tarefas_disponiveis = [tarefa for tarefa in tarefas_copia if tarefa.tempo_chegada <= tempo_atual and tarefa.tempo_restante > 0]
        
        if tarefas_disponiveis:
            tarefas_disponiveis.sort(key=lambda x: x.tempo_restante)
            tarefa_selecionada = tarefas_disponiveis[0]
            
            if tarefa_atual != tarefa_selecionada:
                if tarefa_atual and tarefa_atual.tempo_restante > 0:
                    pass
                
                tarefa_atual = tarefa_selecionada
                if tarefa_atual.tempo_inicio is None:
                    tarefa_atual.tempo_inicio = tempo_atual
            
            tarefa_atual.tempo_restante -= 1
            tempo_atual += 1
            
            if tarefa_atual.tempo_restante == 0:
                tarefa_atual.tempo_fim = tempo_atual
                tarefa_atual.tempo_espera = tarefa_atual.tempo_fim - tarefa_atual.tempo_chegada - tarefa_atual.duracao
                tarefas_agendadas.append(tarefa_atual)
                completadas += 1
        else:
            tempo_atual += 1
    
    for tarefa in tarefas_agendadas:
        tarefa.tempo_espera = tarefa.tempo_fim - tarefa.tempo_chegada - tarefa.duracao
    
    return tarefas_agendadas

def escalonamento_rr(tarefas, quantum):
    tarefas_copia = [Tarefa(tarefa.nome, tarefa.tempo_chegada, tarefa.duracao, tarefa.prioridade) for tarefa in tarefas]
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
        
        if fila_prontos:
            tarefa = fila_prontos.pop(0)
            
            if tarefa.tempo_inicio is None:
                tarefa.tempo_inicio = tempo_atual
            
            tempo_execucao = min(quantum, tarefa.tempo_restante)
            
            tarefa.tempo_restante -= tempo_execucao
            tempo_atual += tempo_execucao
            
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
    
    tempo_total_retorno = sum(tarefa.tempo_fim - tarefa.tempo_chegada for tarefa in tarefas_agendadas)
    tempo_total_espera = sum(tarefa.tempo_espera for tarefa in tarefas_agendadas)
    
    tempo_medio_retorno = tempo_total_retorno / n
    tempo_medio_espera = tempo_total_espera / n
    
    return tempo_medio_retorno, tempo_medio_espera

def mostrar_agendamento(tarefas_agendadas, nome_algoritmo):
    print(f"\n=== {nome_algoritmo} ===")
    print("Tarefa | Chegada | Duração | Início | Fim | Turnaround | Espera")
    print("-" * 65)
    
    for tarefa in tarefas_agendadas:
        turnaround = tarefa.tempo_fim - tarefa.tempo_chegada
        print(f"{tarefa.nome:6} | {tarefa.tempo_chegada:7} | {tarefa.duracao:7} | {tarefa.tempo_inicio:6} | {tarefa.tempo_fim:3} | {turnaround:10} | {tarefa.tempo_espera:5}")

def terminal_interativo():
    tarefas = []
    
    print("=== TERMINAL DE ESCALONAMENTO DE TAREFAS ===")
    print("Comandos:")
    print("  add - Adicionar uma nova tarefa")
    print("  list - Listar tarefas cadastradas")
    print("  clear - Limpar todas as tarefas")
    print("  run - Executar escalonamento")
    print("  exit - Sair do programa")
    print()
    
    while True:
        comando = input("Digite um comando: ").strip().lower()
        
        if comando == "add":
            nome = input("Nome da tarefa: ")
            try:
                chegada = int(input("Tempo de chegada: "))
                duracao = int(input("Duração: "))
                tarefa = Tarefa(nome, chegada, duracao)
                tarefas.append(tarefa)
                print(f"Tarefa {nome} adicionada!")
            except ValueError:
                print("Erro: Digite valores numéricos para tempo e duração!")
        
        elif comando == "list":
            if not tarefas:
                print("Nenhuma tarefa cadastrada.")
            else:
                print("\nTarefas cadastradas:")
                print("Nome | Chegada | Duração")
                print("-" * 20)
                for tarefa in tarefas:
                    print(f"{tarefa.nome:4} | {tarefa.tempo_chegada:7} | {tarefa.duracao:7}")
        
        elif comando == "clear":
            tarefas.clear()
            print("Todas as tarefas foram removidas.")
        
        elif comando == "run":
            if not tarefas:
                print("Erro: Nenhuma tarefa cadastrada!")
                continue
            
            print("\nAlgoritmos disponíveis:")
            print("1 - FCFS (First-Come, First-Served)")
            print("2 - SJF (Shortest Job First)")
            print("3 - SRTF (Shortest Remaining Time First)")
            print("4 - Round Robin")
            
            try:
                opcao = int(input("Escolha o algoritmo (1-4): "))
                
                if opcao == 1:
                    resultado = escalonamento_fcfs(tarefas)
                    mostrar_agendamento(resultado, "FCFS")
                    turnaround, espera = calcular_metricas(resultado)
                    print(f"Tempo médio de turnaround: {turnaround:.2f}")
                    print(f"Tempo médio de espera: {espera:.2f}")
                
                elif opcao == 2:
                    resultado = escalonamento_sjf(tarefas)
                    mostrar_agendamento(resultado, "SJF")
                    turnaround, espera = calcular_metricas(resultado)
                    print(f"Tempo médio de turnaround: {turnaround:.2f}")
                    print(f"Tempo médio de espera: {espera:.2f}")
                
                elif opcao == 3:
                    resultado = escalonamento_srtf(tarefas)
                    mostrar_agendamento(resultado, "SRTF")
                    turnaround, espera = calcular_metricas(resultado)
                    print(f"Tempo médio de turnaround: {turnaround:.2f}")
                    print(f"Tempo médio de espera: {espera:.2f}")
                
                elif opcao == 4:
                    try:
                        quantum = int(input("Digite o quantum para Round Robin: "))
                        resultado = escalonamento_rr(tarefas, quantum)
                        mostrar_agendamento(resultado, f"Round Robin (quantum={quantum})")
                        turnaround, espera = calcular_metricas(resultado)
                        print(f"Tempo médio de turnaround: {turnaround:.2f}")
                        print(f"Tempo médio de espera: {espera:.2f}")
                    except ValueError:
                        print("Erro: Quantum deve ser um número inteiro!")
                
                else:
                    print("Erro: Opção inválida!")
            
            except ValueError:
                print("Erro: Digite um número de 1 a 4!")
        
        elif comando == "exit":
            print("Saindo do programa...")
            break
        
        else:
            print("Comando inválido! Use: add, list, clear, run ou exit")
        
        print()

if __name__ == "__main__":
    terminal_interativo()
