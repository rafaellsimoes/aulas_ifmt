import socket
import time
from urllib.parse import urlparse

class TransportLayerAnalyzer:

    def __init__(self, timeout=5):
        self.timeout = timeout

    # -----------------------------
    # Resolução de DNS
    # -----------------------------
    def resolve_host(self, hostname):
        try:
            ip = socket.gethostbyname(hostname)
            print(f"Resolução DNS: {hostname} → {ip}")
            return ip
        except Exception as e:
            print(f"Erro ao resolver DNS: {e}")
            return None

    # -----------------------------
    # Teste de porta TCP (3-way handshake)
    # -----------------------------
    def test_tcp_port(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            start = time.time()
            result = sock.connect_ex((ip, port))
            end = time.time()
            
            rtt = (end - start) * 1000
            
            if result == 0:
                print(f"   Porta TCP {port} aberta (RTT ≈ {rtt:.2f} ms)")
                sock.close()
                return True
            else:
                print(f"   Porta TCP {port} fechada ou filtrada")
                return False

        except Exception as e:
            print(f"   Erro TCP: {e}")
            return False

    # -----------------------------
    # Teste simples de UDP (sem handshake)
    # -----------------------------
    def test_udp_port(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)

            start = time.time()
            sock.sendto(b"test", (ip, port))
            
            try:
                sock.recvfrom(1024)
                end = time.time()
                print(f"   Porta UDP {port} possivelmente aberta (RTT ≈ {(end-start)*1000:.2f} ms)")
            except socket.timeout:
                print(f"   UDP {port}: sem resposta (indeterminado)")

        except Exception as e:
            print(f"   Erro UDP: {e}")

    # -----------------------------
    # Análise principal
    # -----------------------------
    def analyze(self, url):

        print("\n" + "="*60)
        print(f"ANALISADOR DE CAMADA DE TRANSPORTE")
        print(f"Alvo: {url}")
        print("="*60)

        parsed = urlparse(url if url.startswith("http") else "http://" + url)
        hostname = parsed.hostname

        print(f"\nHost detectado: {hostname}")

        ip = self.resolve_host(hostname)
        if not ip:
            return
        
        print("\nTestando portas TCP comuns:")
        for port in [80, 443, 21, 22, 25, 53, 110, 143, 3306, 5432]:
            self.test_tcp_port(ip, port)

        print("\nTestando UDP (DNS e NTP):")
        self.test_udp_port(ip, 53)
        self.test_udp_port(ip, 123)

def main():
    analyzer = TransportLayerAnalyzer()

    while True:
        target = input("\nDigite o host ou URL (ou 'sair'): ")

        if target.lower() in ["sair", "exit", "quit"]:
            break

        analyzer.analyze(target)

if __name__ == "__main__":
    main()
