import random
from typing import List, Tuple, Optional

class BlocoMemoria:
    def __init__(self, inicio: int, tamanho: int, processo: str = None, tamanho_processo: int = 0):
        self.inicio = inicio
        self.tamanho = tamanho
        self.fim = inicio + tamanho - 1
        self.processo = processo
        self.tamanho_processo = tamanho_processo  # Tamanho real do processo
        self.fragmentacao_interna = 0
    
    def __str__(self):
        if self.processo:
            status = f"Processo: {self.processo} (Usa: {self.tamanho_processo})"
            frag = f" | Frag. Interna: {self.fragmentacao_interna}"
        else:
            status = "LIVRE"
            frag = ""
        return f"[{self.inicio:4d}-{self.fim:4d}] | Tamanho: {self.tamanho:4d} | {status}{frag}"
    
    def __repr__(self):
        return self.__str__()

class GerenciadorMemoriaFragmentacaoInterna:
    def __init__(self, tamanho_total: int, tamanho_pagina: int = 64):
        self.tamanho_total = tamanho_total
        self.tamanho_pagina = tamanho_pagina
        self.memoria = [BlocoMemoria(0, tamanho_total)]
        self.ultima_alocacao = 0
        self.estatisticas = {
            'total_alocacoes': 0,
            'fragmentacao_interna_total': 0,
            'memoria_perdida_total': 0,
            'alocacoes_com_fragmentacao': 0
        }
    
    def mostrar_memoria(self):
        print("\n" + "="*80)
        print("ESTADO ATUAL DA MEMÓRIA - FOCO NA FRAGMENTAÇÃO INTERNA")
        print("="*80)
        print(f"Tamanho da página: {self.tamanho_pagina}")
        print("-" * 80)
        
        for bloco in self.memoria:
            print(bloco)
        
        self._mostrar_estatisticas()
        print("=" * 80)
    
    def _mostrar_estatisticas(self):
        print("\n--- ESTATÍSTICAS DE FRAGMENTAÇÃO INTERNA ---")
        print(f"Total de alocações: {self.estatisticas['total_alocacoes']}")
        print(f"Alocações com fragmentação interna: {self.estatisticas['alocacoes_com_fragmentacao']}")
        print(f"Fragmentação interna total acumulada: {self.estatisticas['fragmentacao_interna_total']}")
        print(f"Memória total perdida: {self.estatisticas['memoria_perdida_total']}")
        
        if self.estatisticas['total_alocacoes'] > 0:
            percentual = (self.estatisticas['alocacoes_com_fragmentacao'] / self.estatisticas['total_alocacoes']) * 100
            print(f"Percentual de alocações com fragmentação: {percentual:.1f}%")
    
    def calcular_paginas_necessarias(self, tamanho_processo: int) -> Tuple[int, int]:
        """Calcula quantas páginas são necessárias e a fragmentação interna resultante"""
        paginas = (tamanho_processo + self.tamanho_pagina - 1) // self.tamanho_pagina
        tamanho_alocado = paginas * self.tamanho_pagina
        fragmentacao = tamanho_alocado - tamanho_processo
        return paginas, fragmentacao
    
    def first_fit(self, tamanho_processo: int, processo: str) -> bool:
        paginas, fragmentacao = self.calcular_paginas_necessarias(tamanho_processo)
        tamanho_necessario = paginas * self.tamanho_pagina
        
        for i, bloco in enumerate(self.memoria):
            if bloco.processo is None and bloco.tamanho >= tamanho_necessario:
                return self._alocar_com_fragmentacao_interna(i, tamanho_processo, tamanho_necessario, fragmentacao, processo)
        return False
    
    def best_fit(self, tamanho_processo: int, processo: str) -> bool:
        paginas, fragmentacao = self.calcular_paginas_necessarias(tamanho_processo)
        tamanho_necessario = paginas * self.tamanho_pagina
        
        melhor_idx = -1
        melhor_tamanho = float('inf')
        
        for i, bloco in enumerate(self.memoria):
            if bloco.processo is None and bloco.tamanho >= tamanho_necessario:
                if bloco.tamanho < melhor_tamanho:
                    melhor_tamanho = bloco.tamanho
                    melhor_idx = i
        
        if melhor_idx != -1:
            return self._alocar_com_fragmentacao_interna(melhor_idx, tamanho_processo, tamanho_necessario, fragmentacao, processo)
        return False
    
    def worst_fit(self, tamanho_processo: int, processo: str) -> bool:
        paginas, fragmentacao = self.calcular_paginas_necessarias(tamanho_processo)
        tamanho_necessario = paginas * self.tamanho_pagina
        
        melhor_idx = -1
        melhor_tamanho = -1
        
        for i, bloco in enumerate(self.memoria):
            if bloco.processo is None and bloco.tamanho >= tamanho_necessario:
                if bloco.tamanho > melhor_tamanho:
                    melhor_tamanho = bloco.tamanho
                    melhor_idx = i
        
        if melhor_idx != -1:
            return self._alocar_com_fragmentacao_interna(melhor_idx, tamanho_processo, tamanho_necessario, fragmentacao, processo)
        return False
    
    def _alocar_com_fragmentacao_interna(self, index: int, tamanho_processo: int, 
                                       tamanho_alocado: int, fragmentacao: int, processo: str) -> bool:
        bloco = self.memoria[index]
        self.estatisticas['total_alocacoes'] += 1
        self.estatisticas['fragmentacao_interna_total'] += fragmentacao
        self.estatisticas['memoria_perdida_total'] += fragmentacao
        
        if fragmentacao > 0:
            self.estatisticas['alocacoes_com_fragmentacao'] += 1
            print(f"Fragmentação interna detectada: {fragmentacao} bytes perdidos")
        
        if bloco.tamanho == tamanho_alocado:
            bloco.processo = processo
            bloco.tamanho_processo = tamanho_processo
            bloco.fragmentacao_interna = fragmentacao
        else:
            novo_bloco_livre = BlocoMemoria(
                bloco.inicio + tamanho_alocado, 
                bloco.tamanho - tamanho_alocado
            )
            bloco.tamanho = tamanho_alocado
            bloco.fim = bloco.inicio + tamanho_alocado - 1
            bloco.processo = processo
            bloco.tamanho_processo = tamanho_processo
            bloco.fragmentacao_interna = fragmentacao
            
            self.memoria.insert(index + 1, novo_bloco_livre)
        
        return True
    
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
    
    def liberar_processo(self, processo: str) -> bool:
        liberado = False
        for bloco in self.memoria:
            if bloco.processo == processo:
                bloco.processo = None
                bloco.tamanho_processo = 0
                bloco.fragmentacao_interna = 0
                liberado = True
        
        if liberado:
            self.compactar_memoria()
        
        return liberado
    
    def liberar_tudo(self):
        for bloco in self.memoria:
            bloco.processo = None
            bloco.tamanho_processo = 0
            bloco.fragmentacao_interna = 0
        self.compactar_memoria()
        self._resetar_estatisticas()
    
    def _resetar_estatisticas(self):
        self.estatisticas = {
            'total_alocacoes': 0,
            'fragmentacao_interna_total': 0,
            'memoria_perdida_total': 0,
            'alocacoes_com_fragmentacao': 0
        }

class SimuladorFragmentacaoInterna:
    def __init__(self, tamanho_memoria: int = 1024, tamanho_pagina: int = 64):
        self.gerenciador = GerenciadorMemoriaFragmentacaoInterna(tamanho_memoria, tamanho_pagina)
        self.processos_ativos = {}
    
    def executar_alocacao(self, algoritmo_num: int, tamanho: int, processo: str) -> bool:
        algoritmos = {
            1: ('First Fit', self.gerenciador.first_fit),
            2: ('Best Fit', self.gerenciador.best_fit),
            3: ('Worst Fit', self.gerenciador.worst_fit)
        }
        
        if algoritmo_num not in algoritmos:
            print(f"Algoritmo {algoritmo_num} não reconhecido!")
            return False
        
        nome_algoritmo, funcao_alocacao = algoritmos[algoritmo_num]
        print(f"\nTentando alocar com {nome_algoritmo}...")
        
        # Calcular páginas necessárias antes da alocação
        paginas, fragmentacao = self.gerenciador.calcular_paginas_necessarias(tamanho)
        print(f"Processo precisa de {tamanho} bytes -> {paginas} páginas ({paginas * self.gerenciador.tamanho_pagina} bytes alocados)")
        
        sucesso = funcao_alocacao(tamanho, processo)
        
        if sucesso:
            self.processos_ativos[processo] = tamanho
            print(f"Processo '{processo}' alocado com sucesso")
            if fragmentacao > 0:
                print(f" Fragmentação interna: {fragmentacao} bytes perdidos")
        else:
            print(f"Falha ao alocar processo '{processo}' - Memória insuficiente")
        
        return sucesso
    
    def liberar_processo(self, processo: str):
        if self.gerenciador.liberar_processo(processo):
            if processo in self.processos_ativos:
                del self.processos_ativos[processo]
            print(f"Processo '{processo}' liberado")
        else:
            print(f"Processo '{processo}' não encontrado")
    
    def demonstrar_efeito_tamanho_pagina(self):
        """Demonstra como o tamanho da página afeta a fragmentação interna"""
        print("\n" + "="*70)
        print("DEMONSTRAÇÃO DO EFEITO DO TAMANHO DA PÁGINA")
        print("="*70)
        
        processos = [47, 129, 73, 255, 18, 300]
        tamanhos_pagina = [32, 64, 128, 256]
        
        for tamanho_pagina in tamanhos_pagina:
            print(f"\n--- Tamanho de Página: {tamanho_pagina} bytes ---")
            total_fragmentacao = 0
            total_memoria_alocada = 0
            
            for i, tamanho_processo in enumerate(processos):
                paginas = (tamanho_processo + tamanho_pagina - 1) // tamanho_pagina
                memoria_alocada = paginas * tamanho_pagina
                fragmentacao = memoria_alocada - tamanho_processo
                
                total_fragmentacao += fragmentacao
                total_memoria_alocada += memoria_alocada
                
                print(f"Processo {i+1}: {tamanho_processo:3d} bytes -> "
                      f"{paginas:2d} páginas -> {memoria_alocada:3d} bytes alocados -> "
                      f"{fragmentacao:3d} bytes perdidos ({fragmentacao/tamanho_pagina*100:5.1f}% da página)")
            
            eficiencia = (total_memoria_alocada - total_fragmentacao) / total_memoria_alocada * 100
            print(f"\nRESUMO - Eficiência: {eficiencia:.1f}% | Fragmentação total: {total_fragmentacao} bytes")
    
    def simular_cenario_fragmentacao(self):
        print("\n" + "="*60)
        print("CENÁRIO DE FRAGMENTAÇÃO INTERNA")
        print("="*60)
        
        # Processos com tamanhos que causam fragmentação interna significativa
        operacoes = [
            (1, 47, 'P1'),   # Precisará de 1 página de 64 -> 17 bytes perdidos
            (2, 129, 'P2'),  # Precisará de 3 páginas de 64 -> 63 bytes perdidos
            (3, 73, 'P3'),   # Precisará de 2 páginas de 64 -> 55 bytes perdidos
            (1, 255, 'P4'),  # Precisará de 4 páginas de 64 -> 1 byte perdido
            (2, 18, 'P5'),   # Precisará de 1 página de 64 -> 46 bytes perdidos
        ]
        
        for algoritmo_num, tamanho, processo in operacoes:
            algoritmos_nomes = {1: 'FIRST FIT', 2: 'BEST FIT', 3: 'WORST FIT'}
            print(f"\n>>> Alocando {processo} ({tamanho} bytes) com {algoritmos_nomes[algoritmo_num]}")
            self.executar_alocacao(algoritmo_num, tamanho, processo)
        
        self.gerenciador.mostrar_memoria()
        
        print("\n>>> Liberando processos P2 e P4")
        self.liberar_processo('P2')
        self.liberar_processo('P4')
        self.gerenciador.mostrar_memoria()

def menu_fragmentacao_interna():
    try:
        tamanho = int(input("Tamanho total da memória (padrão 1024): ") or "1024")
        tamanho_pagina = int(input("Tamanho da página (padrão 64): ") or "64")
    except ValueError:
        tamanho = 1024
        tamanho_pagina = 64
        print("Usando valores padrão: Memória=1024, Página=64")
    
    simulador = SimuladorFragmentacaoInterna(tamanho, tamanho_pagina)
    
    while True:
        print("\n" + "="*60)
        print("SIMULADOR DE FRAGMENTAÇÃO INTERNA")
        print("="*60)
        print("1. Alocar processo")
        print("2. Liberar processo")
        print("3. Mostrar estado da memória")
        print("4. Executar cenário de fragmentação")
        print("5. Demonstrar efeito do tamanho da página")
        print("6. Liberar toda memória")
        print("7. Sair")
        print("="*60)
        
        opcao = input("\nEscolha uma opção (1-7): ").strip()
        
        if opcao == '1':
            print("\n--- ALOCAR PROCESSO ---")
            print("Algoritmos disponíveis:")
            print("1 - First Fit")
            print("2 - Best Fit") 
            print("3 - Worst Fit")
            
            try:
                algoritmo = int(input("Número do algoritmo (1-3): "))
                if algoritmo not in [1, 2, 3]:
                    print("Erro: Escolha um número entre 1 e 3!")
                    continue
                    
                processo = input("Nome do processo: ").strip()
                if not processo:
                    print("Erro: Nome do processo não pode ser vazio!")
                    continue
                    
                tamanho = int(input("Tamanho real do processo (bytes): "))
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
            simulador.simular_cenario_fragmentacao()
            
        elif opcao == '5':
            simulador.demonstrar_efeito_tamanho_pagina()
            
        elif opcao == '6':
            simulador.gerenciador.liberar_tudo()
            simulador.processos_ativos.clear()
            print("Toda a memória foi liberada e estatísticas resetadas")
            
        elif opcao == '7':
            print("Saindo do simulador...")
            break
            
        else:
            print("Opção inválida! Escolha um número de 1 a 7.")

if __name__ == "__main__":
    print("BEM-VINDO AO SIMULADOR DE FRAGMENTAÇÃO INTERNA")
    print("Este simulador foca na análise da fragmentação interna em sistemas de paginação")
    print("=" * 70)
    menu_fragmentacao_interna()
