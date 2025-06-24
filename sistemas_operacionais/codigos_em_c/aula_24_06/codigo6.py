import psutil

def soma(a, b):
    resultado = a + b
    return resultado

def mostrar_info_processo():
    try:
        processo = psutil.Process()
        print("\nInformações do processo:")
        print(f"PID: {processo.pid}")
        print(f"Nome: {processo.name()}")
        print(f"Status: {processo.status()}")
        print(f"Uso de CPU: {processo.cpu_percent()}%")

        mem_info = processo.memory_info()
        print("\nMemória:")
        print(f"RSS (Memória física usada): {mem_info.rss / 1024 / 1024:.2f} MB")
        print(f"VMS (Memória virtual usada): {mem_info.vms / 1024 / 1024:.2f} MB")

        print("\nEndereços de objetos Python na memória:")
        print(f"Endereço da função soma: {hex(id(soma))}")

    except Exception as e:
        print(f"\nErro ao obter informações do processo: {e}")

if __name__ == "__main__":
    # Processo da Função soma
    print("Processo da Soma")
    resultado = soma(5, 3)
    mostrar_info_processo()
    print(f"Endereço do resultado: {hex(id(resultado))}")
