import heapq
from time import sleep

class Paciente:
    def __init__(self, nome, prioridade, tempo_atendimento):
        self.nome = nome
        self.prioridade = prioridade  # 1=emergência, 5=rotina
        self.tempo_atendimento = tempo_atendimento
        self.tempo_espera = 0  # Para controle do aging
    
    def __lt__(self, outro):
        # Prioridade efetiva considera tempo de espera (aging)
        return (self.prioridade - self.tempo_espera) < (outro.prioridade - outro.tempo_espera)

class FilaAtendimento:
    def __init__(self):
        self._fila = []
        self._indice = 0
    
    def inserir(self, paciente):
        # Prioridade efetiva diminui com o tempo de espera
        prioridade_efetiva = paciente.prioridade - paciente.tempo_espera
        heapq.heappush(self._fila, (prioridade_efetiva, self._indice, paciente))
        self._indice += 1
    
    def atender_proximo(self):
        if not self.esta_vazia():
            return heapq.heappop(self._fila)[2]
        raise IndexError("Não há pacientes na fila")
    
    def esta_vazia(self):
        return len(self._fila) == 0
    
    def incrementar_espera(self):
        for i in range(len(self._fila)):
            self._fila[i][2].tempo_espera += 1
    
    def __str__(self):
        return "\n".join([f"{p.nome} (Urgência: {p.prioridade}, Espera: {p.tempo_espera} ciclos)" 
                         for _, _, p in sorted(self._fila)])

def sistema_hospitalar():
    fila = FilaAtendimento()
    
    # Cadastro de pacientes (nome, prioridade, tempo necessário)
    pacientes = [
        Paciente("Paciente A - Fratura exposta", 1, 4),
        Paciente("Paciente B - Dor no peito", 1, 3),
        Paciente("Paciente C - Hemorragia", 1, 5),
        Paciente("Paciente D - Dor abdominal intensa", 2, 2),
        Paciente("Paciente E - Febre alta", 3, 2),
        Paciente("Paciente F - Check-up", 5, 1)
    ]
    
    for p in pacientes:
        fila.inserir(p)
    
    tempo_atendimento = 2  # Tempo por ciclo de atendimento
    ciclo = 0
    
    print("=== Sistema de Atendimento Hospitalar com Prioridade Dinâmica ===")
    print("Fila inicial:")
    print(fila)
    
    while not fila.esta_vazia():
        ciclo += 1
        print(f"\n--- Ciclo {ciclo} ---")
        
        # Aplica aging a todos os pacientes
        fila.incrementar_espera()
        
        # Atende o próximo paciente
        paciente = fila.atender_proximo()
        
        print(f"Atendendo: {paciente.nome} (Urgência: {paciente.prioridade}, Espera: {paciente.tempo_espera} ciclos)")
        
        # Simula o atendimento
        paciente.tempo_atendimento -= tempo_atendimento
        
        # Se ainda precisa de atendimento, recoloca na fila
        if paciente.tempo_atendimento > 0:
            print(f"  {paciente.nome} ainda precisa de {paciente.tempo_atendimento} ciclos")
            fila.inserir(paciente)
        else:
            print(f"  ALTA MÉDICA para {paciente.nome}")
        
        print("\nFila atual:")
        print(fila if not fila.esta_vazia() else "Todos pacientes atendidos!")
        sleep(1.5)  # Pausa para visualização

if __name__ == "__main__":
    sistema_hospitalar()
