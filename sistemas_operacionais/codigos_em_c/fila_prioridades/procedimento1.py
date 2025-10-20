import heapq

class FilaPrioridade:
    def __init__(self):
        self._fila = []
        self._indice = 0
    
    def inserir(self, item, prioridade):
        heapq.heappush(self._fila, (-prioridade, self._indice, item))
        self._indice += 1
    
    def remover(self):
        if not self.esta_vazia():
            return heapq.heappop(self._fila)[-1]
        raise IndexError("A fila de prioridades está vazia")
    
    def esta_vazia(self):
        return len(self._fila) == 0
    
    def __str__(self):
        return str([(-prioridade, item) for prioridade, _, item in sorted(self._fila)])


def sistema_hospitalar():
    fp = FilaPrioridade()
    # Adiciona pacientes com prioridades (5 = emergência, 4 = muito urgente, 
    # 3 = urgente, 2 = pouco urgente, 1 = rotina)
    fp.inserir("Paciente A - Fratura exposta", 1)
    fp.inserir("Paciente B - Check-up anual", 5)
    fp.inserir("Paciente C - Dor no peito", 1)
    fp.inserir("Paciente D - Dor de cabeça", 3)
    fp.inserir("Paciente E - Resfriado", 4)
    fp.inserir("Paciente F - Corte superficial", 4)
    print("Ordem de atendimento:")
    while not fp.esta_vazia():
        print(f"Atendendo: {fp.remover()}")


def main():
    print("=== Sistema Hospitalar ===")
    sistema_hospitalar()


if __name__ == "__main__":
    main()
