import requests
from urllib.parse import urlparse, urlunparse
import socket
import ssl
import json
from datetime import datetime

class HTTPAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def normalize_url(self, url):
        if not url.startswith(('http://', 'https://')):
            try:
                test_url = 'https://' + url
                response = requests.head(test_url, timeout=5, allow_redirects=True)
                return response.url
            except:
                try:
                    test_url = 'http://' + url
                    response = requests.head(test_url, timeout=5, allow_redirects=True)
                    return response.url
                except:
                    return 'https://' + url
        return url
    
    def get_ip_address(self, hostname):
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return "Não foi possível resolver o endereço IP"
    
    def analyze_ssl_certificate(self, hostname, port=443):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    print("🔐 INFORMAÇÕES SSL/TLS:")
                    print(f"   Protocolo: {ssock.version()}")
                    print(f"   Cifra: {ssock.cipher()[0]}")
                    
                    if cert:
                        print(f"   Válido de: {cert['notBefore']}")
                        print(f"   Válido até: {cert['notAfter']}")
                        if 'subjectAltName' in cert:
                            print("   Nomes alternativos:", [name[1] for name in cert['subjectAltName'] if name[0] == 'DNS'])
        except Exception as e:
            print(f"   ❌ SSL não disponível ou erro: {e}")
    
    def analyze_http_structure(self, url):
        try:
            print(f"\n{'='*60}")
            print(f"🔍 ANALISANDO: {url}")
            print(f"{'='*60}")
            
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            
            print(f"\n🌐 INFORMAÇÕES DA URL:")
            print(f"   Esquema: {parsed_url.scheme}")
            print(f"   Hostname: {hostname}")
            print(f"   Porta: {parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)}")
            print(f"   Path: {parsed_url.path or '/'}")
            print(f"   Query: {parsed_url.query}")
            print(f"   Fragmento: {parsed_url.fragment}")
            
            ip_address = self.get_ip_address(hostname)
            print(f"   📡 Endereço IP: {ip_address}")
            
            if parsed_url.scheme == 'https':
                self.analyze_ssl_certificate(hostname)
            
            print(f"\n📨 FAZENDO REQUISIÇÃO HTTP...")
            start_time = datetime.now()
            
            response = self.session.get(
                url, 
                timeout=15,
                allow_redirects=True,
                stream=True
            )
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            print(f"\n✅ RESPOSTA RECEBIDA:")
            print(f"   Status: {response.status_code} {response.reason}")
            print(f"   Tempo de resposta: {response_time:.2f} segundos")
            print(f"   URL final: {response.url}")
            
            if response.history:
                print(f"\n🔄 REDIRECIONAMENTOS:")
                for i, redirect in enumerate(response.history, 1):
                    print(f"   {i}. {redirect.status_code} {redirect.url}")
            
            print(f"\n📋 CABEÇALHOS DA RESPOSTA:")
            for header, value in response.headers.items():
                print(f"   {header}: {value}")
            
            print(f"\n📦 INFORMAÇÕES DO CONTEÚDO:")
            print(f"   Tamanho: {len(response.content)} bytes")
            print(f"   Encoding: {response.encoding}")
            print(f"   Tipo de conteúdo: {response.headers.get('content-type', 'desconhecido')}")
            
            if response.cookies:
                print(f"\n🍪 COOKIES:")
                for cookie in response.cookies:
                    print(f"   {cookie.name}: {cookie.value} (domínio: {cookie.domain})")
            
            print(f"\n🛠️  TECNOLOGIAS DETECTADAS:")
            server = response.headers.get('server', '').lower()
            powered_by = response.headers.get('x-powered-by', '').lower()
            
            if 'apache' in server:
                print("   Servidor: Apache")
            elif 'nginx' in server:
                print("   Servidor: Nginx")
            elif 'iis' in server:
                print("   Servidor: Microsoft IIS")
            
            if 'php' in powered_by:
                print("   PHP detectado")
            if 'asp.net' in powered_by:
                print("   ASP.NET detectado")
            if 'wordpress' in response.text.lower():
                print("   WordPress detectado")
            
            print(f"\n📄 PRIMEIROS 500 CARACTERES DO CONTEÚDO:")
            content_preview = response.text[:500]
            print(f"   {content_preview}")
            
            try:
                json_data = response.json()
                print(f"\n📊 CONTEÚDO JSON DETECTADO:")
                print(f"   Estrutura: {list(json_data.keys()) if isinstance(json_data, dict) else 'Array'}")
            except:
                pass
                
        except requests.exceptions.RequestException as e:
            print(f"\n❌ ERRO NA REQUISIÇÃO: {e}")
        except Exception as e:
            print(f"\n❌ ERRO INESPERADO: {e}")
    
    def test_http_methods(self, url):
        print(f"\n⚡ TESTANDO MÉTODOS HTTP EM: {url}")
        methods = ['GET', 'HEAD', 'OPTIONS']
        
        for method in methods:
            try:
                response = self.session.request(method, url, timeout=10)
                print(f"   {method}: {response.status_code} {response.reason}")
                
                if method == 'OPTIONS' and 'allow' in response.headers:
                    print(f"     Métodos permitidos: {response.headers['allow']}")
                    
            except requests.exceptions.RequestException as e:
                print(f"   {method}: Erro - {e}")

def main():
    analyzer = HTTPAnalyzer()
    
    print("🌐 ANALISADOR HTTP COMPLETO")
    print("=" * 50)
    print("Exemplos: ifmt.edu.br, g1.com.br, google.com, httpbin.org")
    print("=" * 50)
    
    while True:
        try:
            url_input = input("\n🔗 Digite a URL para analisar (ou 'sair' para terminar): ").strip()
            
            if url_input.lower() in ['sair', 'exit', 'quit']:
                break
            if not url_input:
                continue
            
            normalized_url = analyzer.normalize_url(url_input)
            print(f"📡 URL normalizada: {normalized_url}")
            
            analyzer.analyze_http_structure(normalized_url)
            
            analyzer.test_http_methods(normalized_url)
            
        except KeyboardInterrupt:
            print("\n\n👋 Programa encerrado pelo usuário")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
