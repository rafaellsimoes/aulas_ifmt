from collections import OrderedDict
import datetime

class LRUSimulador:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.cache = OrderedDict()
        self.page_faults = 0
        self.hits = 0
        self.historico = []
    
    def acessar_pagina(self, pagina):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        if pagina in self.cache:
            
            self.cache.move_to_end(pagina)
            self.hits += 1
            resultado = "HIT"
            print(f" HIT! Página {pagina} já estava na memória")
        else:
            
            self.page_faults += 1
            resultado = "MISS"
            
            if len(self.cache) >= self.capacidade:
              
                lru_pagina, _ = self.cache.popitem(last=False)
                print(f" PAGE FAULT! Substituída página {lru_pagina} (LRU) por {pagina}")
            else:
                print(f" PAGE FAULT! Adicionada página {pagina} em moldura livre")
            
            
            self.cache[pagina] = timestamp
        
      
        self.historico.append({
            'pagina': pagina,
            'timestamp': timestamp,
            'resultado': resultado,
            'cache_atual': list(self.cache.keys())
        })
        
        self.exibir_estado()
        return resultado
    
    def exibir_estado(self):
        print(f" Molduras: {list(self.cache.keys())}")
        print(f" Ordem (LRU → MRU): {list(self.cache.keys())}")
        print("-" * 50)
    
    def relatorio_final(self):
        total_acessos = self.page_faults + self.hits
        taxa_hits = (self.hits / total_acessos * 100) if total_acessos > 0 else 0
        taxa_faults = (self.page_faults / total_acessos * 100) if total_acessos > 0 else 0
        
        print(f"\n=== RELATÓRIO FINAL ===")
        print(f" Capacidade do cache: {self.capacidade}")
        print(f" Total de acessos: {total_acessos}")
        print(f" Hits: {self.hits} ({taxa_hits:.1f}%)")
        print(f"Page Faults: {self.page_faults} ({taxa_faults:.1f}%)")
        print(f" Estado final do cache: {list(self.cache.keys())}")

def simular_localidade_temporal():
    print("=== SIMULAÇÃO LRU - LOCALIDADE TEMPORAL ===\n")
    
    capacidade = 4
    sequencia = [1, 2, 3, 1, 4, 2, 5, 1, 2, 3,2,1,1,4,5,4,1,2,3,1]
    
    print(f" Número de molduras: {capacidade}")
    print(f" Sequência de referência: {sequencia}")
    print("\n" + "="*60)
    

    simulador = LRUSimulador(capacidade)
    
    for pagina in sequencia:
        simulador.acessar_pagina(pagina)
    

    simulador.relatorio_final()
    
    return simulador

if __name__ == "__main__":
    simular_localidade_temporal()
