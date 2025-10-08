
# ------------------------------------------------------------
# COMPARADOR DE ALGORITMOS DE CRIPTOGRAFIA SIMÉTRICA
# ------------------------------------------------------------
# Este código realiza testes de desempenho e segurança entre os
# algoritmos AES, 3DES e DES utilizando diferentes modos e tamanhos
# de chave. Ele mede o tempo médio de cifragem e decifragem,
# verifica integridade e apresenta recomendações.
#
# Antes de executar, instale a biblioteca:
# pip install pycryptodome
# ------------------------------------------------------------

from Crypto.Cipher import AES, DES, DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time
import sys

class CipherComparator:
    def __init__(self):
        # Geração de chaves para cada algoritmo
        self.aes_key_128 = get_random_bytes(16)   # AES-128 (16 bytes)
        self.aes_key_256 = get_random_bytes(32)   # AES-256 (32 bytes)
        self.tdes_key_2k = get_random_bytes(16)   # 3DES com 2 chaves (112 bits)
        self.tdes_key_3k = get_random_bytes(24)   # 3DES com 3 chaves (168 bits)
        self.des_key = get_random_bytes(8)        # DES (56 bits)
        
    def cipher_aes(self, data, key_size=128, mode=AES.MODE_ECB):
        """Executa cifragem com AES"""
        key = self.aes_key_128 if key_size == 128 else self.aes_key_256
        
        if mode == AES.MODE_ECB:
            cipher = AES.new(key, AES.MODE_ECB)
            encrypted = cipher.encrypt(pad(data, AES.block_size))
            return encrypted, None
        else:
            iv = get_random_bytes(16)
            cipher = AES.new(key, mode, iv)
            encrypted = cipher.encrypt(pad(data, AES.block_size))
            return encrypted, iv
    
    def cipher_3des(self, data, key_type='3k', mode=DES3.MODE_ECB):
        """Executa cifragem com Triple DES (3DES)"""
        key = self.tdes_key_3k if key_type == '3k' else self.tdes_key_2k
        
        if mode == DES3.MODE_ECB:
            cipher = DES3.new(key, DES3.MODE_ECB)
            encrypted = cipher.encrypt(pad(data, DES3.block_size))
            return encrypted, None
        else:
            iv = get_random_bytes(8)
            cipher = DES3.new(key, mode, iv)
            encrypted = cipher.encrypt(pad(data, DES3.block_size))
            return encrypted, iv
    
    def cipher_des(self, data, mode=DES.MODE_ECB):
        """Executa cifragem com DES"""
        if mode == DES.MODE_ECB:
            cipher = DES.new(self.des_key, DES.MODE_ECB)
            encrypted = cipher.encrypt(pad(data, DES.block_size))
            return encrypted, None
        else:
            iv = get_random_bytes(8)
            cipher = DES.new(self.des_key, mode, iv)
            encrypted = cipher.encrypt(pad(data, DES.block_size))
            return encrypted, iv
    
    def benchmark_algorithms(self, data, iterations=100):
        """Executa testes de desempenho dos algoritmos"""
        print("INICIANDO BENCHMARK DE ALGORITMOS")
        print("=" * 60)
        
        results = []
        test_cases = [
            ("AES-128 ECB", self.cipher_aes, {"key_size": 128, "mode": AES.MODE_ECB}),
            ("AES-256 ECB", self.cipher_aes, {"key_size": 256, "mode": AES.MODE_ECB}),
            ("AES-128 CBC", self.cipher_aes, {"key_size": 128, "mode": AES.MODE_CBC}),
            ("3DES 2K ECB", self.cipher_3des, {"key_type": "2k", "mode": DES3.MODE_ECB}),
            ("3DES 3K ECB", self.cipher_3des, {"key_type": "3k", "mode": DES3.MODE_ECB}),
            ("3DES 3K CBC", self.cipher_3des, {"key_type": "3k", "mode": DES3.MODE_CBC}),
            ("DES ECB", self.cipher_des, {"mode": DES.MODE_ECB}),
            ("DES CBC", self.cipher_des, {"mode": DES.MODE_CBC}),
        ]
        
        for name, cipher_func, params in test_cases:
            print(f"Testando {name}...")
            
            # Medição do tempo de cifragem
            start_time = time.time()
            for i in range(iterations):
                encrypted, iv = cipher_func(data, **params)
            encrypt_time = (time.time() - start_time) / iterations
            
            # Medição do tempo de decifragem
            start_time = time.time()
            for i in range(iterations):
                if params.get("mode", AES.MODE_ECB) in [AES.MODE_ECB, DES3.MODE_ECB, DES.MODE_ECB]:
                    # Modos sem IV (ECB)
                    if name.startswith("AES"):
                        cipher = AES.new(self.aes_key_128 if "128" in name else self.aes_key_256, params["mode"])
                    elif name.startswith("3DES"):
                        key = self.tdes_key_2k if "2K" in name else self.tdes_key_3k
                        cipher = DES3.new(key, params["mode"])
                    else:  # DES
                        cipher = DES.new(self.des_key, params["mode"])
                    
                    decrypted = unpad(cipher.decrypt(encrypted),
                                      AES.block_size if "AES" in name else DES3.block_size)
                else:
                    # Modos com IV (CBC)
                    if name.startswith("AES"):
                        cipher = AES.new(self.aes_key_128 if "128" in name else self.aes_key_256, params["mode"], iv)
                    elif name.startswith("3DES"):
                        key = self.tdes_key_2k if "2K" in name else self.tdes_key_3k
                        cipher = DES3.new(key, params["mode"], iv)
                    else:  # DES
                        cipher = DES.new(self.des_key, params["mode"], iv)
                    
                    decrypted = unpad(cipher.decrypt(encrypted),
                                      AES.block_size if "AES" in name else DES3.block_size)
            
            decrypt_time = (time.time() - start_time) / iterations
            
            # Verificação de integridade
            integrity_ok = (decrypted == data)
            
            results.append({
                "algorithm": name,
                "encrypt_time": encrypt_time,
                "decrypt_time": decrypt_time,
                "encrypted_size": len(encrypted),
                "integrity_ok": integrity_ok,
                "security_bits": self._get_security_bits(name)
            })
        
        return results
    
    def _get_security_bits(self, algorithm_name):
        """Retorna os bits de segurança de cada algoritmo"""
        security_bits = {
            "AES-128 ECB": 128,
            "AES-256 ECB": 256,
            "AES-128 CBC": 128,
            "3DES 2K ECB": 112,
            "3DES 3K ECB": 168,
            "3DES 3K CBC": 168,
            "DES ECB": 56,
            "DES CBC": 56
        }
        return security_bits.get(algorithm_name, "N/A")
    
    def print_comparison_table(self, results):
        """Imprime uma tabela comparativa dos resultados"""
        print("\n" + "=" * 90)
        print("TABELA COMPARATIVA - AES vs 3DES vs DES")
        print("=" * 90)
        print(f"{'ALGORITMO':<15} {'SEGURANÇA':<10} {'CIFRAR (ms)':<12} {'DECIFRAR (ms)':<14} {'TAMANHO':<10} {'INTEGRIDADE':<12}")
        print("-" * 90)
        
        for result in results:
            encrypt_ms = result["encrypt_time"] * 1000
            decrypt_ms = result["decrypt_time"] * 1000
            
            print(f"{result['algorithm']:<15} {result['security_bits']:<10} "
                  f"{encrypt_ms:<12.4f} {decrypt_ms:<14.4f} "
                  f"{result['encrypted_size']:<10} {'OK' if result['integrity_ok'] else 'ERRO':<12}")
    
    def print_recommendations(self, results):
        """Imprime recomendações baseadas nos testes"""
        print("\n" + "=" * 60)
        print("RECOMENDAÇÕES DE SEGURANÇA")
        print("=" * 60)
        
        fastest_encrypt = min(results, key=lambda x: x["encrypt_time"])
        fastest_decrypt = min(results, key=lambda x: x["decrypt_time"])
        most_secure = max(results, key=lambda x: x["security_bits"])
        
        print(f"Mais rápido (cifração): {fastest_encrypt['algorithm']} ({fastest_encrypt['encrypt_time']*1000:.4f} ms)")
        print(f"Mais rápido (decifração): {fastest_decrypt['algorithm']} ({fastest_decrypt['decrypt_time']*1000:.4f} ms)")
        print(f"Mais seguro: {most_secure['algorithm']} ({most_secure['security_bits']} bits)")
        
        print("\nCLASSIFICAÇÃO:")
        print("- Para segurança máxima: AES-256")
        print("- Para compatibilidade: 3DES 3K") 
        print("- DES não é recomendado para dados sensíveis")
        print("- Evitar modo ECB para dados com padrões")

def test_different_data_sizes():
    """Executa testes com diferentes tamanhos de dados"""
    comparator = CipherComparator()
    
    data_sizes = [
        (b"Pequeno", "Pequeno (16B)"),
        (b"IFMT - Campus Cel Octayde Jorge da Silva", "Médio (45B)"),
        (b"X+Y" * 100, "Grande"),
        (b"Y" * 1024, "1KB"),
    ]
    
    for data, description in data_sizes:
        print(f"\n{'#' * 70}")
        print(f"TESTE COM DADOS: {description}")
        print(f"Tamanho: {len(data)} bytes")
        print(f"{'#' * 70}")
        
        results = comparator.benchmark_algorithms(data, iterations=50)
        comparator.print_comparison_table(results)
        comparator.print_recommendations(results)

def demo_simple_comparison():
    """Executa uma demonstração simples"""
    print("EXERCÍCIO 1: COMPARADOR DE ALGORITMOS")
    print("=" * 50)
    
    comparator = CipherComparator()
    
    # Dados de teste
    test_data = b"IFMT - Campus Cel Octayde - Dados confidenciais para teste de algoritmos criptograficos!"
    
    print(f"Dados de teste: {test_data.decode()}")
    print(f"Tamanho dos dados: {len(test_data)} bytes")
    print(f"Iteracoes por teste: 100")
    
    # Executar o benchmark
    results = comparator.benchmark_algorithms(test_data, iterations=100)
    
    # Mostrar resultados
    comparator.print_comparison_table(results)
    comparator.print_recommendations(results)
    
    # Teste de integridade detalhado
    print("\n" + "=" * 50)
    print("VERIFICAÇÃO DE INTEGRIDADE DETALHADA")
    print("=" * 50)
    
    for result in results:
        status = "INTEGRO" if result["integrity_ok"] else "CORROMPIDO"
        print(f"{result['algorithm']:<15}: {status}")

if __name__ == "__main__":
    # Executa demonstração simples
    demo_simple_comparison()
    
    # Testes adicionais com diferentes tamanhos
    print("\n\n" + "=" * 80)
    print("TESTES ADICIONAIS COM DIFERENTES TAMANHOS DE DADOS")
    print("=" * 80)
    
    resposta = input("Deseja executar testes com diferentes tamanhos de dados? (s/n): ")
    if resposta.lower() == 's':
        test_different_data_sizes()
