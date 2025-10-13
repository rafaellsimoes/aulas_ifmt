import random
from typing import List, Tuple, Optional

class BlocoMemoria:
    def __init__(self, inicio: int, tamanho: int, processo: str = None):
        self.inicio = inicio
        self.tamanho = tamanho
        self.fim = inicio + tamanho - 1
        self.processo = processo
    
    def __str__(self):
        status = f"Processo: {self.processo}" if self.processo else "LIVRE"
        return f"[{self.inicio:4d}-{self.fim:4d}] | Tamanho: {self.tamanho:4d} | {status}"
    
    def __repr__(self):
        return self.__str__()

class GerenciadorMemoria:
    def __init__(self, tamanho_total: int):
        self.tamanho_total = tamanho_total
        self.memoria = [BlocoMemoria(0, tamanho_total)]
        self.ultima_alocacao = 0
    
    def mostrar_memoria(self):
        print("\n" + "="*60)
        print("ESTADO ATUAL DA MEMÓRIA")
        print("="*60)
        for bloco in self.memoria:
            print(bloco)
        print(f"Espaço total: {self.tamanho_total}")
        print(f"Espaço livre: {self.calcular_espaco_livre()}")
        print(f"Fragmentação: {self.calcular_fragmentacao():.2f}%")
        print("="*60)
    
    def calcular_espaco_livre(self) -> int:
        return sum(bloco.tamanho for bloco in self.memoria if bloco.processo is None)
    
    def calcular_fragmentacao(self) -> float:
        espaco_livre = self.calcular_espaco_livre()
        if espaco_livre == 0:
            return 0.0
        
        blocos_livres = [bloco for bloco in self.memoria if bloco.processo is None]
        maior_bloco_livre = max(bloco.tamanho for bloco in blocos_livres) if blocos_livres else 0
        
        if maior_bloco_livre == 0:
            return 100.0
        
        return ((espaco_livre - maior_bloco_livre) / espaco_livre) * 100
    
    def compactar_memoria(self):
        i = 0
        while i < len(self.memoria) - 1:
            bloco_atual = self.memoria[i]
            bloco_proximo = self.memoria[i + 1]
            
            if bloco_atual.processo is None and bloco_proximo.processo is None:
                novo_tamanho = bloco_atual.tamanho + bloco_proximo.tamanho
                self.memoria[i] = BlocoMemoria(bloco_atual.inicio, novo_tamanho)
                self.memoria.pop(i + 1)
            else:
                i += 1
    
    def first_fit(self, tamanho: int, processo: str) -> bool:
        for i, bloco in enumerate(self.memoria):
            if bloco.processo is None and bloco.tamanho >= tamanho:
                self._alocar_bloco(i, tamanho, processo)
                self.ultima_alocacao = i
                return True
        return False
    
    def next_fit(self, tamanho: int, processo: str) -> bool:
        n = len(self.memoria)
        for i in range(n):
            idx = (self.ultima_alocacao + i) % n
            bloco = self.memoria[idx]
            if bloco.processo is None and bloco.tamanho >= tamanho:
                self._alocar_bloco(idx, tamanho, processo)
                self.ultima_alocacao = idx
                return True
        return False
    
    def best_fit(self, tamanho: int, processo: str) -> bool:
        melhor_idx = -1
        melhor_tamanho = float('inf')
        
        for i, bloco in enumerate(self.memoria):
            if bloco.processo is None and bloco.tamanho >= tamanho:
                if bloco.tamanho < melhor_tamanho:
                    melhor_tamanho = bloco.tamanho
                    melhor_idx = i
        
        if melhor_idx != -1:
            self._alocar_bloco(melhor_idx, tamanho, processo)
            self.ultima_alocacao = melhor_idx
            return True
        return False
    
    def worst_fit(self, tamanho: int, processo: str) -> bool:
        melhor_idx = -1
        melhor_tamanho = -1
        
        for i, bloco in enumerate(self.memoria):
            if bloco.processo is None and bloco.tamanho >= tamanho:
                if bloco.tamanho > melhor_tamanho:
                    melhor_tamanho = bloco.tamanho
                    melhor_idx = i
        
        if melhor_idx != -1:
            self._alocar_bloco(melhor_idx, tamanho, processo)
            self.ultima_alocacao = melhor_idx
            return True
        return False
    
    def _alocar_bloco(self, index: int, tamanho: int, processo: str):
        bloco = self.memoria[index]
        
        if bloco.tamanho == tamanho:
            bloco.processo = processo
        else:
            novo_bloco_livre = BlocoMemoria(
                bloco.inicio + tamanho, 
                bloco.tamanho - tamanho
            )
            bloco.tamanho = tamanho
            bloco.fim = bloco.inicio + tamanho - 1
            bloco.processo = processo
            self.memoria.insert(index + 1, novo_bloco_livre)
    
    def liberar_processo(self, processo: str) -> bool:
        liberado = False
        for bloco in self.memoria:
            if bloco.processo == processo:
                bloco.processo = None
                liberado = True
        
        if liberado:
            self.compactar_memoria()
        
        return liberado
    
    def liberar_tudo(self):
        for bloco in self.memoria:
            bloco.processo = None
        self.compactar_memoria()

class SimuladorMemoria:
    def __init__(self, tamanho_memoria: int = 1024):
        self.gerenciador = GerenciadorMemoria(tamanho_memoria)
        self.processos_ativos = {}
    
    def executar_alocacao(self, algoritmo_num: int, tamanho: int, processo: str) -> bool:
        algoritmos = {
            1: ('First Fit', self.gerenciador.first_fit),
            2: ('Next Fit', self.gerenciador.next_fit),
            3: ('Best Fit', self.gerenciador.best_fit),
            4: ('Worst Fit', self.gerenciador.worst_fit)
        }
        
        if algoritmo_num not in algoritmos:
            print(f"Algoritmo {algoritmo_num} não reconhecido!")
            return False
        
        nome_algoritmo, funcao_alocacao = algoritmos[algoritmo_num]
        print(f"\nTentando alocar com {nome_algoritmo}...")
        
        sucesso = funcao_alocacao(tamanho, processo)
        
        if sucesso:
            self.processos_ativos[processo] = tamanho
            print(f"Processo '{processo}' alocado com sucesso ({tamanho} unidades)")
        else:
            print(f"Falha ao alocar processo '{processo}' ({tamanho} unidades) - Memória insuficiente")
        
        return sucesso
    
    def liberar_processo(self, processo: str):
        if self.gerenciador.liberar_processo(processo):
            if processo in self.processos_ativos:
                del self.processos_ativos[processo]
            print(f"Processo '{processo}' liberado")
        else:
            print(f"Processo '{processo}' não encontrado")
    
    def simular_cenario(self):
        print("\n" + "="*50)
        print("INICIANDO SIMULAÇÃO DE CENÁRIO")
        print("="*50)
        
        operacoes = [
            (1, 100, 'P1'),
            (3, 200, 'P2'),
            (4, 50, 'P3'),
            (2, 150, 'P4'),
            (1, 300, 'P5'),
            (3, 75, 'P6')
        ]
        
        for algoritmo_num, tamanho, processo in operacoes:
            algoritmos_nomes = {
                1: 'FIRST FIT', 
                2: 'NEXT FIT', 
                3: 'BEST FIT', 
                4: 'WORST FIT'
            }
            print(f"\n>>> Tentando alocar {processo} ({tamanho} unidades) com {algoritmos_nomes[algoritmo_num]}")
            self.executar_alocacao(algoritmo_num, tamanho, processo)
            self.gerenciador.mostrar_memoria()
        
        print("\n>>> Liberando processos P2 e P4")
        self.liberar_processo('P2')
        self.liberar_processo('P4')
        self.gerenciador.mostrar_memoria()
        
        print("\n>>> Tentando alocar P7 (180 unidades) com BEST FIT após fragmentação")
        self.executar_alocacao(3, 180, 'P7')
        self.gerenciador.mostrar_memoria()

def menu_interativo():
    try:
        tamanho = int(input("Tamanho total da memória (padrão 1024): ") or "1024")
    except ValueError:
        tamanho = 1024
        print("Usando valor padrão: 1024")
    
    simulador = SimuladorMemoria(tamanho)
    
    while True:
        print("\n" + "="*50)
        print("SIMULADOR DE GERENCIAMENTO DE MEMÓRIA")
        print("="*50)
        print("1. Alocar processo")
        print("2. Liberar processo")
        print("3. Mostrar estado da memória")
        print("4. Executar cenário de teste")
        print("5. Liberar toda memória")
        print("6. Sair")
        print("="*50)
        
        opcao = input("\nEscolha uma opção (1-6): ").strip()
        
        if opcao == '1':
            print("\n--- ALOCAR PROCESSO ---")
            print("Algoritmos disponíveis:")
            print("1 - First Fit")
            print("2 - Next Fit") 
            print("3 - Best Fit")
            print("4 - Worst Fit")
            
            try:
                algoritmo = int(input("Número do algoritmo (1-4): "))
                if algoritmo not in [1, 2, 3, 4]:
                    print("Erro: Escolha um número entre 1 e 4!")
                    continue
                    
                processo = input("Nome do processo: ").strip()
                if not processo:
                    print("Erro: Nome do processo não pode ser vazio!")
                    continue
                    
                tamanho = int(input("Tamanho do processo: "))
                if tamanho <= 0:
                    print("Erro: Tamanho deve ser maior que zero!")
                    continue
                    
                simulador.executar_alocacao(algoritmo, tamanho, processo)
                
            except ValueError:
                print("Erro: Digite um número válido!")
                
        elif opcao == '2':
            print("\n--- LIBERAR PROCESSO ---")
            processo = input("Nome do processo a liberar: ").strip()
            if processo:
                simulador.liberar_processo(processo)
            else:
                print("Erro: Nome do processo não pode ser vazio!")
            
        elif opcao == '3':
            simulador.gerenciador.mostrar_memoria()
            
        elif opcao == '4':
            simulador.simular_cenario()
            
        elif opcao == '5':
            simulador.gerenciador.liberar_tudo()
            simulador.processos_ativos.clear()
            print("Toda a memória foi liberada")
            
        elif opcao == '6':
            print("Saindo do simulador...")
            break
            
        else:
            print("Opção inválida! Escolha um número de 1 a 6.")

if __name__ == "__main__":
    print("BEM-VINDO AO SIMULADOR DE GERENCIAMENTO DE MEMÓRIA")
    print("Este simulador implementa os algoritmos: First Fit, Next Fit, Best Fit e Worst Fit")
    menu_interativo()
